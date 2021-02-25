# -*- coding: utf-8 -*-
from change_task.models.task import (SceneTask, CustomTask)
from rest_framework import serializers


class SceneSerializer(serializers.ModelSerializer):
    class Meta:
        model = SceneTask
        fields = ("id",)


class SceneTaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = SceneTask
        fields = '__all__'
        # depth = 1


class CustomTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomTask
        # fields = '__all__'
        exclude = ('creator', 'updated_by', 'is_deleted')
        read_only_fields = ('status', )
