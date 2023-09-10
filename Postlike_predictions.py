from app import db
from flask_login import login_user, login_required, logout_user, current_user
from models import User, Post, Bot_of_User, Hashtags, Post_hashtags, User_likes_to_post, Comment


def Calculate_post_Tensor(post):
    if post:
        tensor = []
        #every post tensor should have the same axis on the same place
        hashtags_of_post = Post_hashtags.query.filter_by(post_id=post.id).all()
        hashtags_o_post_id = []
        for hashtag_of_post in hashtags_of_post:
            hashtags_o_post_id.append(hashtag_of_post.hashtag_id)

        for hashtag in Hashtags.query.all():
            if hashtag.id in hashtags_o_post_id:
                tensor.append(1)
            else:
                tensor.append(0)
        #Calulate the range of the tensor to 1 (tensor_length is the length of the tensor in a n demensional space)
        tensor_length = 0
        for i in range(len(tensor)):
            tensor_length += tensor[i]**2
        tensor_length = tensor_length**(1/2)
        if tensor_length == 0:
            tensor_length = 1
        #now the tensor_length is the length of the tensor in a n demensional space
        for i in range(len(tensor)):
            tensor[i] = tensor[i]/tensor_length
        #now the tensor is normalized
    else:
        print("This post don\'t exist!")
        return None
    return tensor

def Calculate_posts_Tensor(posts):
    posts_tensor = []
    for post in posts:
        posts_tensor.append(Calculate_post_Tensor(post))
    return posts_tensor

def Calculate_user_Tensor(user):
    if user:
        tensor = []
           #every user tensor should have the same axis on the same place
        posts_likes_of_user_ids = User_likes_to_post.query.filter_by(user_id=user.id).all()
        posts_likes_of_user = []

        for posts_likes_of_user_id in posts_likes_of_user_ids:
            if posts_likes_of_user_id.post_id:
                posts_likes_of_user.append(Post.query.filter_by(id=posts_likes_of_user_id.post_id).first())

        print(posts_likes_of_user)
        posts_likes_of_user_tensors = Calculate_posts_Tensor(posts_likes_of_user)

        for posts_likes_of_user_tensor in posts_likes_of_user_tensors:
            if len(tensor) < 1:
                tensor = posts_likes_of_user_tensor
            else:
                for i in range(len(tensor)):
                    tensor[i] += posts_likes_of_user_tensor[i]
        #Calulate the range of the tensor to 1 (tensor_length is the length of the tensor in a n demensional space)
        tensor_length = 0
        for i in range(len(tensor)):
            tensor_length += tensor[i]**2
        tensor_length = tensor_length**(1/2)
        print(tensor_length)
        if tensor_length == 0:
            print("This user don\'t like any posts!")
            return None
        for i in range(len(tensor)):
            tensor[i] = tensor[i]/tensor_length
        #now the tensor is normalized
    else:
        print("This user don\'t exist!")
        return None
    return tensor

def Calculate_distance(user_tensor, post_tensor):
    if user_tensor and post_tensor:
        distance = 0
        for i in range(len(user_tensor)):
            distance += (user_tensor[i]-post_tensor[i])**2
        distance = distance**(1/2)
    else:
        print("One of the tensors don\'t exist!")
        return None
    return distance

#create a 2d array with the post and the distance between the user and the post
def Create_post_Tensor_Array(posts, user):
    posts_tensor = Calculate_posts_Tensor(posts)
    user_tensor = Calculate_user_Tensor(user)
    if user_tensor:
        post_tensor_array = []
        for i in range(len(posts_tensor)):
            post_tensor_array.append([posts[i], Calculate_distance(user_tensor, posts_tensor[i])])
        return post_tensor_array
    else:
        return None

#sort the post_tensor_array by the distance with the bubble sort algorithm
def Sort_post_Tensor_Array(post_tensor_array):
    if post_tensor_array:
        for i in range(len(post_tensor_array)):
            for j in range(len(post_tensor_array)):
                if post_tensor_array[i][1] < post_tensor_array[j][1]:
                    post_tensor_array[i], post_tensor_array[j] = post_tensor_array[j], post_tensor_array[i]
        return post_tensor_array
    else:
        return None

def predict_posts(user, posts):

    post_tensor_array = Create_post_Tensor_Array(posts, user)
    print(post_tensor_array)

    if post_tensor_array:
        post_tensor_array = Sort_post_Tensor_Array(post_tensor_array)
        posts_list = [item[0] for item in post_tensor_array]
        return posts_list
    else:
        return []

