package com.lqd.repository;

/**
 * @ClassName User
 * @Description TODO
 * @Author lqd
 * @Date 2018/12/9 9:28
 * @Version 1.0
 **/
public class User
{
    private Long id;
    private String userName;
    private String address;

    public String getAddress() {
        return address;
    }

    public void setAddress(String address) {
        this.address = address;
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getUserName() {
        return userName;
    }

    public void setUserName(String userName) {
        this.userName = userName;
    }
}
