from django import forms
from rest_framework import serializers
from application.virtualfile.models import VirtualFile


class VirtualFileSerializers(serializers.ModelSerializer):

    class Meta:
        model = VirtualFile
        fields = '__all__'
        read_only_fields = (
            'file_path', 'file_name', 'file_suffix', 'edit_file', 'save_mode', 'update_time', 'status'
        )


class UploadForm(forms.Form):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    dir_id = forms.IntegerField(help_text='associated dir')
