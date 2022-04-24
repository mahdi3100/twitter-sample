$(document).ready(function(){


    $(document).on("click",'#newpost',function(){newpost()});
      $(document).on("click",'.edit',function(){editpost(this)});

      $(document).on("click",".like strong",function(){like(this)});

      setLikesPost();
});

function setLikesPost(){//set like on the post if admin did not like the post , could not do it directly cause the loop

       $(".onepost").each(function(index,element){


          if($(element).find(".like strong").length==0){
                $(element).find(".like").html('<strong>❤️</strong><span>'+$(element).find(".like").attr("data")+'</span>');
          }
       });
}
function like(element){

  fetch('/like', {
      method: 'PUT',
      body: JSON.stringify({
          postid:$(element).parents(".like").attr("post")
      })

    })
    .then(response => response.json())
    .then(response =>{
      if(response["error"]){
          alert(response["error"]);
         return;
      }

      if(response["likedislike"] == "dislike"){
        $(element).html("💔");
        $(element).next().text(parseInt($(element).next().text())+1)
        $(element).parent().attr("data",parseInt(  $(element).parent().attr("data")) +1 )
      }else{
        $(element).html("❤️");
        $(element).next().text(parseInt($(element).next().text())-1)
        $(element).parent().attr("data",parseInt(  $(element).parent().attr("data")) -1 )

      }
    });
}
  function newpost(){
    var textpost= document.querySelector("#textpost").value;

    fetch('/newpost', {
        method: 'POST',
        body: JSON.stringify({
            posttxt:textpost
        })

      })
      .then(response => response.json())
      .then(response => {
        console.log(response)
        if(response["error "]){
            alert(response["error "])
           return;
        }
        $("#textpost").val("");

              var content = '<a href="/profile/'+response["userid"]+'"><h3>'+response["username"]+'</h3></a><strong class="edit" data="'+response["id"]+'">Edit</strong><p>'+textpost+'</p><div class="options"> <div class="like" data="0" post="'+response["id"]+'"><strong class="like" data="'+response["id"]+'">❤️</strong><span>0</span></div><span>Comment</span><span>'+response["date"]+'</span></div>';


              $('#allposts').prepend("<div class='onepost'>"+content+"</div>");
      });
  }

function seteditpost(element){


var getID = $(element).attr("data");
var textpost = $(element).prev().val();

fetch('/editpost', {
   method: 'POST',
   body: JSON.stringify({
       posttxt:textpost,
       postid:getID
   })

 })
 .then(response => response.json())
 .then(response => {
   console.log(response)
   if(response["error "]){
       alert(response["error"])
      return;
   }

 $(element).parents(".onepost").find("textarea").remove();
 $(element).replaceWith("<p>"+textpost+"</p>");


 });
}

  function editpost(element){
      var idPost = $(element).attr("data");
      var getPostText = $(element).parent().find("p").text();

      $("<input type='button' value='Repost' data='"+idPost+"'/>").on("click",function(){seteditpost(this)}).insertAfter(element)
      $(element).parent().find("p").remove()
      $(element).replaceWith("<textarea>"+getPostText+"</textarea>");


   }
