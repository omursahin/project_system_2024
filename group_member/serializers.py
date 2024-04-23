from rest_framework import serializers

from group_member.models import GroupMember


class GroupMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupMember
        fields = '__all__'
