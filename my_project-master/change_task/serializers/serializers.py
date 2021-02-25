# -*- coding: utf-8 -*-
from rest_framework import serializers
from change_task.models import *


class ServicePrividerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServicePrivider
        fields = (
            "id", "name", "description", "checkers", "checkers_type", "approvers", "approvers_type",
            "rule_priority_list")
        required_field = ("name", "description")


class RuleSerializer(serializers.ModelSerializer):
    service_privider = ServicePrividerSerializer()

    class Meta:
        model = Rule
        fields = (
            "id", "name", "description", "is_enable", "condition", "service_privider")
        required_field = ("name", "description", "is_enable", "condition", "service_privider")


class SceneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scene
        fields = '__all__'
