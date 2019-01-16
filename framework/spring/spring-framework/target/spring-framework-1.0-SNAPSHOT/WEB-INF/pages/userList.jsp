<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>
<html>
<body>
   用户列表：
   <c:forEach var="user" items="${userList}">
       <c:out value="${user.userName}"/><br/>
   </c:forEach>
</body>
</html>