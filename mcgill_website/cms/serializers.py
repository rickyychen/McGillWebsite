from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField
from cms.models import Page

class SiteStructureSerializer(serializers.ModelSerializer):
    children = RecursiveField(many=True)

    def update(self,instance,validated_data):
        instance.page_template = validated_data.get('page_template',instance.page_template)
        instance.page_name_en = validated_data.get('page_name_en',instance.page_name_en)
        instance.page_name_fr = validated_data.get('page_name_fr',instance.page_name_fr)
        instance.page_title_en = validated_data.get('page_title_en',instance.page_title_en)
        instance.page_title_fr = validated_data.get('page_title_fr',instance.page_title_fr)
        instance.page_content_en = validated_data.get('page_content_en',instance.page_content_en)
        instance.page_content_fr = validated_data.get('page_content_fr',instance.page_content_fr)
        instance.custom_js_css_en = validated_data.get('custom_js_css_en',instance.custom_js_css_en)
        instance.custom_js_css_fr = validated_data.get('custom_js_css_fr',instance.custom_js_css_fr)
        instance.save()
        return instance

    class Meta:
        model = Page
        fields = ('id','page_level','page_template','page_name_en','page_name_fr','page_title_en','page_title_fr','page_content_en','page_content_fr','custom_js_css_en','custom_js_css_fr','children')
