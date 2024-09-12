// @ts-ignore
import React, { useState, useEffect } from 'react';

type UserDataProps = {
  userId: string;
};

type User = {
  name: string;
  email: string;
};

const UserData: React.FC<UserDataProps> = ({ userId }) => {
  // 使用 useState 来管理组件的状态
  const [user, setUser] = useState<User | null>(null);
  const [seconds, setSeconds] = useState<number>(0);

  // 获取用户数据的函数
  const fetchUserData = () => {
    fetch(`https://secret.url/user/${userId}`)
      .then(response => response.json())
      .then(data => setUser(data))
      .catch(error => console.error('Error fetching user data:', error));
  };

  // 使用 useEffect 模拟 componentDidMount 和 componentDidUpdate
  useEffect(() => {
    fetchUserData();

    // 启动定时器
    const intervalId = setInterval(() => {
      setSeconds(prevSeconds => prevSeconds + 1);
    }, 1000);

    // 清理副作用，模拟 componentWillUnmount
    return () => {
      clearInterval(intervalId);
    };
  }, [userId]);

  return (
    <div>
      <h1>User Data Component</h1>
      {user ? (
        <div>
          <p>Name: {user.name}</p>
          <p>Email: {user.email}</p>
        </div>
      ) : (
        <p>Loading user data...</p>
      )}
      <p>Timer: {seconds} seconds</p>
    </div>
  );
};

export default UserData;
