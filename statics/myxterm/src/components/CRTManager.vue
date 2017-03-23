<template>
    <div class="container-fluid">
        <div class="row">
            <nav class="col-sm-3 col-md-2 sidebar bg-faded">
                <ul class="nav flex-column">
                    <li class="nav-item">
                        <router-link class="nav-link active" to="/crt-manager/machine-list">我的主机</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link class="nav-link" to="/crt-manager/add-remove">添加主机</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link class="nav-link" to="/crt-manager/password">管理主机密码</router-link>
                    </li>
                </ul>
            </nav>
            <!--sidebar-->
            <div class="main-view">
                <router-view></router-view>
            </div>
            
        </div>
        
    </div>
</template>

<style>
.main-view{
    margin-left:35%;
}

.sidebar {
    padding-left: 0;
    padding-right: 0;
    position: fixed;
    top: 51px;
    bottom: 0;
    left: 0;
    z-index: 1000;
    padding: 20px;
    overflow-x: hidden;
    overflow-y: auto;
    border-right: 1px solid #eee;
}

.bg-faded {
    background-color: #f7f7f7;
}
</style>