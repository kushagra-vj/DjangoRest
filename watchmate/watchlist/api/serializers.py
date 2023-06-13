from rest_framework import serializers
from watchlist.models import WatchList, StreamingPlatform, Review

# model serialization
class ReviewSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Review
        exclude = ['watchlist']


class WatchListSerializer(serializers.ModelSerializer):
    review = ReviewSerializer(many=True, read_only=True)
    # title_length = serializers.SerializerMethodField()

    class Meta:
        model = WatchList
        # fields = ['id', 'title', 'storyline', 'platform', 'created']
        fields = '__all__'
        # exclude = ['active']

    # def get_title_length(self, instance):
    #     return len(instance.title)

    def validate(self, instance):
        if instance['title'] == instance['storyline']:
            raise serializers.ValidationError('Title and description should not be same!')
        return instance

    def validate_name(self, name):
        if len(name) < 2:
            raise serializers.ValidationError('Name is too short!')
        else:
            return name


class StreamingPlatformSerializer(serializers.ModelSerializer):
# class StreamingPlatformSerializer(serializers.HyperlinkedModelSerializer):
    watchlist = WatchListSerializer(many=True, read_only=True) # return all mathces of streaming
    # watchlist = serializers.StringRelatedField(many=True) # return names of movie in streaming
    # watchlist = serializers.PrimaryKeyRelatedField(many=True, read_only=True) # return primary key of movie
    # watchlist = serializers.HyperlinkedRelatedField(
    #     many=True,
    #     read_only=True,
    #     view_name='watchlist:movie-list'
    # ) # return Hyperlink of movie in streaming 

    class Meta:
        model = StreamingPlatform
        fields = '__all__'


# serialize.Serializer

# def name_length(name):
#     if len(name) < 2:
#         raise serializers.ValidationError('Name is too short!')
#     else:
#         return name


# class MovieSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(validators=[name_length])
#     description = serializers.CharField()
#     active = serializers.BooleanField()

#     def create(self, validated_data):
#         return Movie.objects.create(**validated_data)
    
#     def update(self, instance, validated_data):
#         instance.name = validated_data.get('name', instance.name)
#         instance.description = validated_data.get('description', instance.description)
#         instance.active = validated_data.get('active', instance.active)
#         instance.save()
#         return instance
    
#     def validate(self, instance):
#         if instance['name'] == instance['description']:
#             raise serializers.ValidationError('Title and description should not be same!')
#         return instance
    
    # filed  validation
    # def validate_name(self, name):
    #     if len(name) < 2:
    #         raise serializers.ValidationError('Name is too short!')
    #     else:
    #         return name

    
