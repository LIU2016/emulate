<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>
<html>
<body>
   <form action="/user/saveUser" method="post">
     <p>user name: <input type="text" name="user.userName" /></p>
     <input type="submit" value="Submit" />
   </form>
</body>
</html>