# coding=utf-8

from rest_framework import serializers

from .. import models


class SharedUrlSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.SharedUrl
        fields = ("email", "url",)


class SharedFileSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.SharedFile
        fields = ("email", "file")

    # def create(self, validated_data):
    #     # validated_data['author'] =
    #     return super().create(validated_data)
