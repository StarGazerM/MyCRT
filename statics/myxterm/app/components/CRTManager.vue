<template>
    <div class="container-fluid">
        <div class="row">
            <nav class="col-sm-3 col-md-2 sidebar bg-faded">
                <ul class="nav flex-column">
                    <li class="nav-item">
                        <a class="nav-link active" href="#">我的主机</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#">添加主机</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#">管理主机密码</a>
                    </li>
                </ul>
            </nav>
            <!--sidebar-->

            <div class="col-auto">
                <router-view></router-view>
            </div>
        </div>
        
    </div>
</template>