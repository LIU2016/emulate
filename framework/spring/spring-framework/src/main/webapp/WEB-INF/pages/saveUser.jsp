<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>
<script src="https://cdn.staticfile.org/jquery/1.10.2/jquery.min.js"></script>
<html>
<body>
   --------------content-type:application/x-www-form-urlcoded----------------
   <form action="/user/saveUser" method="post">
     <p>user name: <input type="text" name="userName" /></p>
     <p>user address: <input type="text" name="address" /></p>
     <input type="submit" value="saveUser00" />
   </form>
   --------------content-type:application/json----------------<br/>
   <a id="saveUser01" href="javascript:;">saveUser01</a>
</body>
<script>
$(document).ready(function(){
  $("#saveUser01").click(function(){
    $.ajax({
        　　　　　　　　url:"/user/saveUser01",
        　　　　　　　　type:"POST",
        　　　　　　　　data:'{"userName":"admin","address":"admin123"}',
        　　　　　　　　contentType:"application/json;charset=UTF-8",
        　　　　　　　　success:function(data){
        　　　　　　　　　　alert("request success ! ");
        　　　　　　　　}
        　　　　});
  });
});


</script>
</html>