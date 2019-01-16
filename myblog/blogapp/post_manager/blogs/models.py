from django.db import models
from .models import TextPost

# Create your models here.

class BlogPost(TextPost):

	def defaultTag():
		return PostTopic.objects.get(tag="None")

	article_title = models.CharField(max_length=200)
	topic = models.ManyToManyField('PostTopic', default=[defaultTag])
	
	def __str__(self):
		return self.author + "\n" + self.pub_date.strftime(" %d/%m/%y_%H:%M") + " " + self.article_title
	
	def save(self):
	
		super(BlogPost, self).save()
		
		if self.status == BlogPost.STATUS.published:
			#Emails users that a new blog post was created
			emailSubList("Aaron's Blog: New Blog Post!", 
				"""Hello there subscriber,
				
				It is I, Aaron, from Aaron's blog, here to tell you that {} has posted a new blog post titled "{}" for everyone to see! Check it out here: {}
				
				Good day!
				
				Aaron
				""".format(self.author, self.article_title, "http://aaronjencks.net/blog/{}".format(self.id)))

class Comment(TextPost):
    blog_target = models.ForeignKey('BlogPost', on_delete=models.CASCADE, blank=True, null=True)
    comment_target = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    pass
