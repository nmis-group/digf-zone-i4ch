from utils import *
from dataset import *
from data_module import *
#from pytorch_lightning.core.decorators import auto_move_data
from numbers import Number
from typing import List
from functools import singledispatch
from fastcore.dispatch import typedispatch

class BoltDetector(pl.LightningModule):
    def __init__(self,
                 df,
                 bs = 2,
                 num_workers = 16,
                 epochs = 50,
                 num_classes=1,
                 img_size=1024,
                 prediction_confidence_threshold=0.2,
                 learning_rate=0.001,
                 wbf_iou_threshold=0.44,
                 inference_transforms=get_valid_transforms(target_img_size=1024),
                 model_architecture='tf_efficientnetv2_l'):
        super().__init__()
        self.df = df
        self.bs = bs
        self.num_workers = num_workers
        self.img_size = img_size
        self.epochs = epochs
        self.num_classes = num_classes
        self.model_architecture = model_architecture
        self.model = self.create_model()
        self.prediction_confidence_threshold = prediction_confidence_threshold
        self.lr = learning_rate
        self.wbf_iou_threshold = wbf_iou_threshold
        self.inference_tfms = inference_transforms
        self.save_hyperparameters()
        
        self.train_transforms = get_train_transforms(target_img_size=self.img_size)
        self.valid_transforms = get_valid_transforms(target_img_size=self.img_size)
        self.inference_transforms = get_valid_transforms(target_img_size=self.img_size)
        
        self.train_dataset = BoltDataset(self.df, self.train_transforms , 'train')
        print(len(self.train_dataset))
        self.valid_dataset = BoltDataset(self.df, self.valid_transforms , 'valid')
        print(len(self.valid_dataset))
        self.test_dataset = BoltDataset(self.df, self.valid_transforms , 'test')
        print(len(self.test_dataset))
        
    @staticmethod
    def collate_fn(batch):
        images, targets, bolts = tuple(zip(*batch))
        images = torch.stack(images)
        images = images.float()

        boxes = [target["bboxes"].float() for target in targets]
        labels = [target["labels"].float() for target in targets]
        img_size = torch.tensor([target["img_size"] for target in targets]).float()
        img_scale = torch.tensor([target["img_scale"] for target in targets]).float()

        annotations = {
            "bbox": boxes,
            "cls": labels,
            "img_size": img_size,
            "img_scale": img_scale,
        }

        return images, annotations, targets, bolts

    def train_dataloader(self):
        self.train_loader = torch.utils.data.DataLoader(
                self.train_dataset,
                batch_size=self.bs,
                shuffle=True,
                pin_memory=True,
                drop_last=True,
                num_workers = self.num_workers,
                collate_fn = self.collate_fn)
        return self.train_loader
    
    def val_dataloader(self):
        self.valid_loader = torch.utils.data.DataLoader(
                self.valid_dataset,
                batch_size=self.bs,
                shuffle=False,
                pin_memory=True,
                drop_last=True,
                num_workers = self.num_workers,
                collate_fn = self.collate_fn)
        return self.valid_loader
    
    def test_dataloader(self):
        self.test_loader = torch.utils.data.DataLoader(
                self.test_dataset,
                batch_size=self.bs,
                shuffle=False,
                pin_memory=True,
                drop_last=True,
                num_workers = self.num_workers,
                collate_fn = self.collate_fn)
        return self.test_loader

    #@auto_move_data
    def forward(self, images, targets):
        return self.model(images, targets)

    def configure_optimizers(self):
        optimizer =  torch.optim.AdamW(self.model.parameters(), lr=self.lr)
#         #scheduler = torch.optim.lr_scheduler.OneCycleLR(optimizer,
#                                                         max_lr=self.lr,
#                                                         steps_per_epoch=len(self.train_dataloader()),
#                                                         epochs=self.epochs)
        return [optimizer]#, [scheduler]
    
    def create_model(self):
        efficientdet_model_param_dict[self.model_architecture] = dict(
            name=self.model_architecture,
            backbone_name=self.model_architecture,
            backbone_args=dict(drop_path_rate=0.2),
            num_classes=self.num_classes,
            url='', )

        config = get_efficientdet_config(self.model_architecture)
        config.update({'num_classes': self.num_classes})
        config.update({'image_size': (self.img_size, self.img_size)})

        print(config)

        net = EfficientDet(config, pretrained_backbone=True)
        net.class_net = HeadNet(config, num_outputs=config.num_classes,)
        check_freeze(net)
        return DetBenchTrain(net, config)


    def training_step(self, batch, batch_idx):
        images, annotations, _, bolts = batch

        losses = self.model(images, annotations)

        logging_losses = {
            "class_loss": losses["class_loss"].detach(),
            "box_loss": losses["box_loss"].detach(),
        }

        self.log("train_loss", losses["loss"], on_step=True, on_epoch=True, prog_bar=True, logger=True)
        self.log("train_class_loss", losses["class_loss"], on_step=True, on_epoch=True, prog_bar=True, logger=True)
        self.log("train_box_loss", losses["box_loss"], on_step=True, on_epoch=True, prog_bar=True, logger=True)

        return losses['loss']


    @torch.no_grad()
    def validation_step(self, batch, batch_idx):
        images, annotations, targets, bolts = batch
        outputs = self.model(images, annotations)

        detections = outputs["detections"]

        (predicted_bboxes, predicted_class_confidences, predicted_class_labels,) = self.post_process_detections(detections)

        batch_predictions = {
            "predictions": detections,
            "targets": targets,
            "bolts_counted": len(predicted_bboxes),
        }

        logging_losses = {
            "class_loss": outputs["class_loss"].detach(),
            "box_loss": outputs["box_loss"].detach(),
        }

        self.log("valid_loss", outputs["loss"], on_step=True, on_epoch=True, prog_bar=True, logger=True, sync_dist=True)
        self.log("valid_class_loss", logging_losses["class_loss"], on_step=True, on_epoch=True, prog_bar=True, logger=True, sync_dist=True )
        self.log("valid_box_loss", logging_losses["box_loss"], on_step=True, on_epoch=True, prog_bar=True, logger=True, sync_dist=True)

        return {'loss': outputs["loss"], 'batch_predictions': batch_predictions}
    
    @typedispatch
    def predict(self, images: List):
        """
        For making predictions from images
        Args:
            images: a list of PIL images

        Returns: a tuple of lists containing bboxes, predicted_class_labels, predicted_class_confidences

        """
        image_sizes = [(image.size[1], image.size[0]) for image in images]
        images_tensor = torch.stack([ self.inference_tfms(
                                      image=np.array(image, dtype=np.float32),
                                      labels=np.ones(1),
                                      bboxes=np.array([[0, 0, 1, 1]]),)["image"]  for image in images])

        return self._run_inference(images_tensor, image_sizes)

    @typedispatch
    def predict(self, images_tensor: torch.Tensor):
        """
        For making predictions from tensors returned from the model's dataloader
        Args:
            images_tensor: the images tensor returned from the dataloader

        Returns: a tuple of lists containing bboxes, predicted_class_labels, predicted_class_confidences

        """
        if images_tensor.ndim == 3:
            images_tensor = images_tensor.unsqueeze(0)
        if (images_tensor.shape[-1] != self.img_size or images_tensor.shape[-2] != self.img_size):
            raise ValueError(f"Input tensors must be of shape (N, 3, {self.img_size}, {self.img_size})")

        num_images = images_tensor.shape[0]
        image_sizes = [(self.img_size, self.img_size)] * num_images

        return self._run_inference(images_tensor, image_sizes)
    
    @typedispatch
    def count_bolts(self, images_tensor: torch.Tensor, bolts):
        """
        For making predictions from tensors returned from the model's dataloader
        Args:
            images_tensor: the images tensor returned from the dataloader

        Returns: a tuple of lists containing bboxes, predicted_class_labels, predicted_class_confidences

        """
        if images_tensor.ndim == 3:
            images_tensor = images_tensor.unsqueeze(0)
        if (images_tensor.shape[-1] != self.img_size or images_tensor.shape[-2] != self.img_size):
            raise ValueError(f"Input tensors must be of shape (N, 3, {self.img_size}, {self.img_size})")

        num_images = images_tensor.shape[0]
        image_sizes = [(self.img_size, self.img_size)] * num_images

        _, _, _, bolts_predicted = self._run_inference_count_bolts(images_tensor, image_sizes)
        
        print('Ground Truth Bolts = {}'.format(bolts))
        print('Predicted Bolts Count = {}'.format(bolts_predicted))

    def _run_inference(self, images_tensor, image_sizes):
        dummy_targets = self._create_dummy_inference_targets(num_images=images_tensor.shape[0])

        detections = self.model(images_tensor.to(self.device), dummy_targets)["detections"]
        (
            predicted_bboxes,
            predicted_class_confidences,
            predicted_class_labels,
        ) = self.post_process_detections(detections)

        scaled_bboxes = self.__rescale_bboxes(predicted_bboxes=predicted_bboxes, image_sizes=image_sizes)

        return scaled_bboxes, predicted_class_labels, predicted_class_confidences
    
    def _run_inference_count_bolts(self, images_tensor, image_sizes):
        dummy_targets = self._create_dummy_inference_targets(num_images=images_tensor.shape[0])

        detections = self.model(images_tensor.to(self.device), dummy_targets)["detections"]
        (
            predicted_bboxes,
            predicted_class_confidences,
            predicted_class_labels,
        ) = self.post_process_detections(detections)

        scaled_bboxes = self.__rescale_bboxes(predicted_bboxes=predicted_bboxes, image_sizes=image_sizes)

        return scaled_bboxes, predicted_class_labels, predicted_class_confidences, len(predicted_class_confidences[0])
    
    def _create_dummy_inference_targets(self, num_images):
        dummy_targets = {
            "bbox": [
                torch.tensor([[0.0, 0.0, 0.0, 0.0]], device=self.device)
                for i in range(num_images)
            ],
            "cls": [torch.tensor([1.0], device=self.device) for i in range(num_images)],
            "img_size": torch.tensor(
                [(self.img_size, self.img_size)] * num_images, device=self.device
            ).float(),
            "img_scale": torch.ones(num_images, device=self.device).float(),
        }

        return dummy_targets
    
    def post_process_detections(self, detections):
        predictions = []
        for i in range(detections.shape[0]):
            predictions.append(
                self._postprocess_single_prediction_detections(detections[i])
            )

        predicted_bboxes, predicted_class_confidences, predicted_class_labels = run_wbf(
            predictions, image_size=self.img_size, iou_thr=self.wbf_iou_threshold
        )

        return predicted_bboxes, predicted_class_confidences, predicted_class_labels

    def _postprocess_single_prediction_detections(self, detections):
        boxes = detections.detach().cpu().numpy()[:, :4]
        scores = detections.detach().cpu().numpy()[:, 4]
        classes = detections.detach().cpu().numpy()[:, 5]
        indexes = np.where(scores > self.prediction_confidence_threshold)[0]
        boxes = boxes[indexes]

        return {"boxes": boxes, "scores": scores[indexes], "classes": classes[indexes]}

    def __rescale_bboxes(self, predicted_bboxes, image_sizes):
        scaled_bboxes = []
        for bboxes, img_dims in zip(predicted_bboxes, image_sizes):
            im_h, im_w = img_dims

            if len(bboxes) > 0:
                scaled_bboxes.append(
                    (
                        np.array(bboxes)
                        * [
                            im_w / self.img_size,
                            im_h / self.img_size,
                            im_w / self.img_size,
                            im_h / self.img_size,
                        ]
                    ).tolist()
                )
            else:
                scaled_bboxes.append(bboxes)

        return scaled_bboxes
    

@patch
def aggregate_prediction_outputs(self: BoltDetector, outputs):

    detections = torch.cat(
        [output["batch_predictions"]["predictions"] for output in outputs]
    )

    image_ids = []
    targets = []
    for output in outputs:
        batch_predictions = output["batch_predictions"]
        #image_ids.extend(batch_predictions["image_ids"])
        targets.extend(batch_predictions["targets"])

    (
        predicted_bboxes,
        predicted_class_confidences,
        predicted_class_labels,
    ) = self.post_process_detections(detections)

    return (
        predicted_class_labels,
        #image_ids,
        predicted_bboxes,
        predicted_class_confidences,
        targets,
    )


@patch
def validation_epoch_end(self: BoltDetector, outputs):
    """Compute and log training loss and accuracy at the epoch level."""

    validation_loss_mean = torch.stack(
        [output["loss"] for output in outputs]
    ).mean()

    (
        predicted_class_labels,
        #image_ids,
        predicted_bboxes,
        predicted_class_confidences,
        targets,
    ) = self.aggregate_prediction_outputs(outputs)

    #truth_image_ids = [target["image_id"].detach().item() for target in targets]
    truth_boxes = [
        target["bboxes"].detach()[:, [1, 0, 3, 2]].tolist() for target in targets
    ] # convert to xyxy for evaluation
    truth_labels = [target["labels"].detach().tolist() for target in targets]

    stats = get_coco_stats(
        #prediction_image_ids=image_ids,
        prediction_image_ids=[1]*len(truth_boxes),
        predicted_class_confidences=predicted_class_confidences,
        predicted_bboxes=predicted_bboxes,
        predicted_class_labels=predicted_class_labels,
        #target_image_ids=truth_image_ids,
        target_image_ids=[1]*len(truth_boxes),
        target_bboxes=truth_boxes,
        target_class_labels=truth_labels,
    )['All']

    return {"val_loss": validation_loss_mean, "metrics": stats}