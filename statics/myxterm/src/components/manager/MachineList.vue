<template>

<div class="row">
    <div class="col">
        <ul class="list-group">
            <li class="list-group-item" v-for="m in machines">
                <div class="row">
                    <div class='col'>
                        {{m['username']}}
                    </div>
                    <div class="col-auto">isOnline?={{m.isOnline}}</div>
                    <div class="col"><button type="button" class="btn btn-warning" v-on:click="setXtermName(m.username)" aria-disabled="{{m.isOnline}}">link</button></div>
                </div>
            </li>
        </ul>
    </div>

</div>


</template>

<script>
    import Bus from '../../bus.js';
    import Config from '../../config.js';

    export default {
        data: function() {
            return {
                machines: []
            }
        },
        mounted: function() {
            fetch( Config.BaseURL + "/u/machine_list", {
                    credentials: 'include',
                })
                .then((response) => {
                    console.log(response)
                    return response.json()
                }).then((data) => {
                    console.log(data[0])
                    this.machines = data
                })
        },

        methods: {
            setXtermName: function(id) {
                Bus.$emit('xtermChange', id)
            }
        }
    }
</script>