<template>

<div class="row">
    <div class="col">
        <div class="input-group">
            <span class="input-group-addon" id="basic-addon1">Username</span>
            <input type="text" class="form-control" placeholder="Username" aria-describedby="basic-addon1" name="username" v-model="username">
        </div>
        <div class="input-group">
            <span class="input-group-addon" id="basic-addon1">password</span>
            <input type="password" class="form-control" placeholder="password" aria-describedby="basic-addon1" username="password" v-model="password">
        </div>
        <button type="button" class="btn btn-warning" v-on:click="submit">ADD</button>
    </div>

</div>

</template>

<script>
    export default{
        data: {
            username: '',
            password: '',
        },
        methods: {
            submit: function(event){
                if(this.username === '' | this.password === ''){
                    return
                } 
                fetch('http://127.0.0.1:8888/u/add_machine', {
                    method: 'POST',
                    body: 'username=' + this.username + '&' + 'password=' + this.password,
                })
            }
        }
    }
</script>

