<template>

<div class="row">
    <div class="col">
        <ul class="list-group">
            <li class="list-group-item" v-for="m in machines">
                <a v-on:click="setXtermName(m.username)">{{m['username']}}</a>
            </li>
        </ul>
    </div>

</div>

</template>

<script>
import Bus from '../../bus.js';

    export default {
        data: function(){
            return {
                machines: []
            }
        },
        created: function(){
            fetch("http://127.0.0.1:8888/u/machine_list", {
                     credentials: 'include'
            })
                    .then((response) => {
                        return response.json();
                    }).then((data) => {
                        console.log(data[0])
                        this.machines = data
                    })
        }
        methods: {
            setXtermName: function(id){
                Bus.$emit('xtermChange', id)
            }
        }
    }
</script>