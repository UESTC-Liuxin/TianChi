# model settings
model = dict(
    type='CascadeRCNN',
    num_stages=3,
    pretrained='torchvision://resnet50',
    backbone=dict(
        type='ResNet',
        depth=50,
        num_stages=4,
        out_indices=(0, 1, 2, 3),
        frozen_stages=1,
        style='pytorch',
        # gen_attention=dict(
        #     spatial_range=-1, num_heads=8, attention_type='0010', kv_stride=2),
        # stage_with_gen_attention=[[], [], [0, 1, 2, 3, 4, 5], [0, 1, 2]],
        dcn=dict(
            type='DCN', deformable_groups=1, fallback_on_stride=False),
        stage_with_dcn=(False, True, True, True)
    ),

    neck=[dict(
        type='FPN',
        in_channels=[256, 512, 1024, 2048],
        out_channels=256,
        num_outs=5),
        # dict(
        #     type='BFP',
        #     in_channels=256,
        #     num_levels=5,
        #     refine_level=2,
        #     refine_type='non_local')
    ],
    rpn_head=dict(
        type='RPNHead',
        in_channels=256,
        feat_channels=256,
        anchor_scales=[11],   #scale
        anchor_ratios=[0.25,0.5,0.7, 1.0,1.33, 2.0,4.0,5.0,10.0],
        anchor_strides=[4, 8, 16, 32, 64],
        target_means=[.0, .0, .0, .0],
        target_stds=[1.0, 1.0, 1.0, 1.0],
        loss_cls=dict(
            type='CrossEntropyLoss', use_sigmoid=True, loss_weight=1.0),
        # loss_cls=dict(
        #     type='FocalLoss', use_sigmoid=True, loss_weight=1.0),# 修改了loss，为了调控难易样本与正负样本比例
        loss_bbox=dict(type='SmoothL1Loss', beta=1.0 / 9.0, loss_weight=1.0)),
    bbox_roi_extractor=dict(
        type='SingleRoIExtractor',
        roi_layer=dict(type='RoIAlign', out_size=7, sample_num=2),
        out_channels=256,
        featmap_strides=[4, 8, 16, 32]),
    bbox_head=[
        dict(
            type='SharedFCBBoxHead',
            num_fcs=2,
            in_channels=256,
            fc_out_channels=1024,
            roi_feat_size=7,
            num_classes=11,
            target_means=[0., 0., 0., 0.],
            target_stds=[0.1, 0.1, 0.2, 0.2],
            reg_class_agnostic=True,
            loss_cls=dict(
                type='CrossEntropyLoss', use_sigmoid=False, loss_weight=1.0),
            loss_bbox=dict(type='SmoothL1Loss', beta=1.0, loss_weight=1.0)),
        dict(
            type='SharedFCBBoxHead',
            num_fcs=2,
            in_channels=256,
            fc_out_channels=1024,
            roi_feat_size=7,
            num_classes=11,
            target_means=[0., 0., 0., 0.],
            target_stds=[0.05, 0.05, 0.1, 0.1],
            reg_class_agnostic=True,
            loss_cls=dict(
                type='CrossEntropyLoss', use_sigmoid=False, loss_weight=1.0),
            loss_bbox=dict(type='SmoothL1Loss', beta=1.0, loss_weight=1.0)),
        dict(
            type='SharedFCBBoxHead',
            num_fcs=2,
            in_channels=256,
            fc_out_channels=1024,
            roi_feat_size=7,
            num_classes=11,
            target_means=[0., 0., 0., 0.],
            target_stds=[0.033, 0.033, 0.067, 0.067],
            reg_class_agnostic=True,
            loss_cls=dict(
                type='CrossEntropyLoss', use_sigmoid=False, loss_weight=1.0),
            loss_bbox=dict(type='SmoothL1Loss', beta=1.0, loss_weight=1.0))
    ])
# model training and testing settings
# train_cfg = dict(
#     rpn=dict(
#         assigner=dict(
#             type='MaxIoUAssigner',
#             pos_iou_thr=0.7,
#             neg_iou_thr=0.3,
#             min_pos_iou=0.3,
#             ignore_iof_thr=-1),
#         sampler=dict(
#             type='RandomSampler',
#             num=256,
#             pos_fraction=0.5,
#             neg_pos_ub=-1,
#             add_gt_as_proposals=False),
#         allowed_border=0,
#         pos_weight=-1,
#         debug=False),
#     rpn_proposal=dict(
#         nms_across_levels=False,
#         nms_pre=2000,
#         nms_post=2000,
#         max_num=2000,
#         nms_thr=0.7,
#         min_bbox_size=0),
#     rcnn=[
#         dict(
#             assigner=dict(
#                 type='MaxIoUAssigner',
#                 pos_iou_thr=0.5, # 更换
#                 neg_iou_thr=0.5,
#                 min_pos_iou=0.5,
#                 ignore_iof_thr=-1),
#             sampler=dict(
#                 type='OHEMSampler',
#                 num=512,
#                 pos_fraction=0.25,
#                 neg_pos_ub=-1,
#                 add_gt_as_proposals=True),
#             pos_weight=-1,
#             debug=False),
#         dict(
#             assigner=dict(
#                 type='MaxIoUAssigner',
#                 pos_iou_thr=0.6,
#                 neg_iou_thr=0.6,
#                 min_pos_iou=0.6,
#                 ignore_iof_thr=-1),
#             sampler=dict(
#                 type='OHEMSampler', # 解决难易样本，也解决了正负样本比例问题。
#                 num=512,
#                 pos_fraction=0.25,
#                 neg_pos_ub=-1,
#                 add_gt_as_proposals=True),
#             pos_weight=-1,
#             debug=False),
#         dict(
#             assigner=dict(
#                 type='MaxIoUAssigner',
#                 pos_iou_thr=0.7,
#                 neg_iou_thr=0.7,
#                 min_pos_iou=0.7,
#                 ignore_iof_thr=-1),
#             sampler=dict(
#                 type='OHEMSampler',
#                 num=512,
#                 pos_fraction=0.25,
#                 neg_pos_ub=-1,
#                 add_gt_as_proposals=True),
#             pos_weight=-1,
#             debug=False)
#     ],
train_cfg = dict(
    rpn=dict(
        assigner=dict(
            type='MaxIoUAssigner',
            pos_iou_thr=0.7,
            neg_iou_thr=0.3,
            min_pos_iou=0.3,
            ignore_iof_thr=-1),
        sampler=dict(
            type='RandomSampler',
            num=256,
            pos_fraction=0.5,
            neg_pos_ub=-1,
            add_gt_as_proposals=False),
        allowed_border=0,
        pos_weight=-1,
        debug=False),
    rpn_proposal=dict(
        nms_across_levels=False,
        nms_pre=2000,
        nms_post=2000,
        max_num=2000,
        nms_thr=0.7,
        min_bbox_size=0),
    rcnn=[
        dict(
            assigner=dict(
                type='MaxIoUAssigner',
                pos_iou_thr=0.5,
                neg_iou_thr=0.5,
                min_pos_iou=0.5,
                ignore_iof_thr=-1),
            sampler=dict(
                type='RandomSampler',
                num=512,
                pos_fraction=0.25,
                neg_pos_ub=-1,
                add_gt_as_proposals=True),
            pos_weight=-1,
            debug=False),
        dict(
            assigner=dict(
                type='MaxIoUAssigner',
                pos_iou_thr=0.6,
                neg_iou_thr=0.6,
                min_pos_iou=0.6,
                ignore_iof_thr=-1),
            sampler=dict(
                type='RandomSampler',
                num=512,
                pos_fraction=0.25,
                neg_pos_ub=-1,
                add_gt_as_proposals=True),
            pos_weight=-1,
            debug=False),
        dict(
            assigner=dict(
                type='MaxIoUAssigner',
                pos_iou_thr=0.7,
                neg_iou_thr=0.7,
                min_pos_iou=0.7,
                ignore_iof_thr=-1),
            sampler=dict(
                type='RandomSampler',
                num=512,
                pos_fraction=0.25,
                neg_pos_ub=-1,
                add_gt_as_proposals=True),
            pos_weight=-1,
            debug=False)
    ],
    stage_loss_weights=[1, 0.5, 0.25])
test_cfg = dict(
    rpn=dict(
        nms_across_levels=False,
        nms_pre=1000,
        nms_post=1000,
        max_num=1000,
        nms_thr=0.7,
        min_bbox_size=0),
    rcnn=dict(
        score_thr=0.0, nms=dict(type='nms', iou_thr=0.5), max_per_img=100))# 这里可以换为sof_tnms
# dataset settings
dataset_type = 'CocoDataset'
data_root = '/home/liusiyu/liuxin/mmdetection/data/coco/'
img_norm_cfg = dict(
    mean=[37.372034, 49.357872, 71.855], std=[49.504940, 57.116612, 79.024876], to_rgb=True)
# train_pipeline = [
#     dict(type='LoadImageFromFile'),
#     dict(type='LoadAnnotations', with_bbox=True),
#     dict(type='Resize', img_scale=(658,492), keep_ratio=True),
#     dict(type='RandomFlip', flip_ratio=0.5),
#     dict(type='Normalize', **img_norm_cfg),
#     dict(type='Pad', size_divisor=32),
#     dict(type='DefaultFormatBundle'),
#     dict(type='Collect', keys=['img', 'gt_bboxes', 'gt_labels']),
# ]
albu_train_transforms = [
    dict(
        type='ShiftScaleRotate',
        shift_limit=(-0.0625, 0.0625),
        scale_limit=(-0.1, 0.1),
        rotate_limit=[-10, 10],
        interpolation=1,
        p=0.5),
    # dict(
    #     type='Rotate',
    #     limit=(-10, 10),
    #     interpolation=1,
    #     p=0.5),
    # dict(
    #     type='RandomBrightnessContrast',
    #     brightness_limit=[0.1, 0.3],
    #     contrast_limit=[0.1, 0.3],
    #     p=0.2),
    # dict(
    #     type='OneOf',
    #     transforms=[
    #         dict(
    #             type='RGBShift',
    #             r_shift_limit=10,
    #             g_shift_limit=10,
    #             b_shift_limit=10,
    #             p=1.0),
    #         dict(
    #             type='HueSaturationValue',
    #             hue_shift_limit=20,
    #             sat_shift_limit=30,
    #             val_shift_limit=20,
    #             p=1.0)
    #     ],
    #     p=0.1),
    # dict(type='JpegCompression', quality_lower=85, quality_upper=95, p=0.2),
    # dict(type='ChannelShuffle', p=0.1),
    # dict(
    #     type='OneOf',
    #     transforms=[
    #         dict(type='Blur', blur_limit=3, p=1.0),
    #         dict(type='MedianBlur', blur_limit=3, p=1.0)
    #     ],
    #     p=0.1),
]
train_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(type='LoadAnnotations', with_bbox=True, with_mask=False),
    dict(type='Resize', img_scale=[(800,400), (800,600)], multiscale_mode='range', keep_ratio=True),
    # dict(type='Resize', img_scale=(658,492), keep_ratio=True),
    dict(type='RandomFlip', flip_ratio=0.5),
    dict(type='Pad', size_divisor=32),
    dict(
        type='Albu',
        transforms=albu_train_transforms,
        bbox_params=dict(
            type='BboxParams',
            format='pascal_voc',
            label_fields=['gt_labels'],
            min_visibility=0.0,
            filter_lost_elements=True),
        keymap={
            'img': 'image',
            # 'gt_masks': 'masks',
            'gt_bboxes': 'bboxes'
        },
        update_pad_shape=False,
        skip_img_without_anno=True),
    dict(type='Normalize', **img_norm_cfg),
    dict(type='DefaultFormatBundle'),
    dict(
        type='Collect',
        keys=['img', 'gt_bboxes', 'gt_labels'],
        meta_keys=('filename', 'ori_shape', 'img_shape', 'img_norm_cfg',
                   'pad_shape', 'scale_factor')
    )
]
test_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(
        type='MultiScaleFlipAug',
        img_scale=(658,492),
        flip=False,
        transforms=[
            dict(type='Resize', keep_ratio=True),
            dict(type='Normalize', **img_norm_cfg),
            dict(type='Pad', size_divisor=32),
            dict(type='ImageToTensor', keys=['img']),
            dict(type='Collect', keys=['img']),
        ])
]
data = dict(
    imgs_per_gpu=8,
    workers_per_gpu=4,
    train=dict(
        type='RepeatDataset',
        times=3,
        dataset=dict(
            type=dataset_type,
        ann_file=data_root + 'annotations/train2017.json',
        img_prefix=data_root + 'images/',
        pipeline=train_pipeline)),
    val=dict(
        type=dataset_type,
        ann_file=data_root + 'annotations/val2017.json',
        img_prefix=data_root + 'images/',
        pipeline=test_pipeline),
    test=dict(
        type=dataset_type,
        ann_file=data_root + 'annotations/test2017.json',
        img_prefix=data_root + 'testimages/',
        pipeline=test_pipeline))
# optimizer
#  single  gpu  and  autoscale
optimizer = dict(type='SGD', lr=0.02, momentum=0.9, weight_decay=0.0001)
optimizer_config = dict(grad_clip=dict(max_norm=35, norm_type=2))
# learning policy
lr_config = dict(
    policy='step',
    warmup='linear',
    warmup_iters=500,
    warmup_ratio=1.0 / 3,
    gamma=0.1,
    step=[8,12,16])
checkpoint_config = dict(interval=1)
# yapf:disable
log_config = dict(
    interval=50,
    hooks=[
        dict(type='TextLoggerHook'),
        # dict(type='TensorboardLoggerHook')
    ])
# yapf:enable
# runtime settings
total_epochs =25
dist_params = dict(backend='nccl')
log_level = 'INFO'
import datetime
a=datetime.datetime.now().strftime('%Y%m%d%H%M')+'_pg'
work_dir = '/home/liusiyu/liuxin/mmdetection/checkpoints/cascade_rcnn_dconv_c3-c5_r50_fpn_1x/{}'.format(a)
load_from = "/home/liusiyu/liuxin/mmdetection/model/cascade_rcnn_dconv_c3-c5_r50_fpn_1x_20190125-dfa53166.pth"
# load_from = "/datassd/yuejian/mmdetection/work_dirs/20200118134853/epoch_12.pth"
resume_from = None
workflow = [
    ('train', 1)]

# tools/dist_train.sh my_configs/pg_baseline.py  2 --validate

#
# tools/dist_test.sh /home/liusiyu/liuxin/mmdetection/my_configs/pg_baseline.py \
# /home/liusiyu/liuxin/mmdetection/checkpoints/cascade_rcnn_dconv_c3-c5_r50_fpn_1x/202002091234_pg/latest.pth 4 \
# --json_out /home/liusiyu/liuxin/mmdetection/checkpoints/cascade_rcnn_dconv_c3-c5_r50_fpn_1x/reslut.json
#
