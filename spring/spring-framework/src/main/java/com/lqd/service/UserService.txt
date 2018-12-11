package com.lqd.service;

import com.lqd.repository.User;
import org.springframework.beans.factory.InitializingBean;
import org.springframework.context.annotation.Lazy;
import org.springframework.context.annotation.Scope;
import org.springframework.stereotype.Service;
import javax.annotation.PostConstruct;
import java.util.ArrayList;
import java.util.List;

/**
 * @ClassName UserService
 * @Description TODO
 * @Author lqd
 * @Date 2018/12/9 9:23
 * @Version 1.0
 **/
@Service
@Scope(value="singleton")
@Lazy
public class UserService implements InitializingBean
{
    public UserService()
    {
        System.out.println("UserService cinit");
    }

    private List<User> userList = new ArrayList<>() ;

    public boolean saveUser(User user)
    {
        return userList.add(user);
    }

    public List<User> getUserList()
    {
        return userList ;
    }

    @PostConstruct
    public void postConstruct(){
        System.out.println("postConstruct");
    }

    @Override
    public void afterPropertiesSet() throws Exception {
        System.out.println("afterPropertiesSet");
    }
}
