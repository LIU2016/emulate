<template>
    <div id="login">
        <h1>{{userName}}</h1>
        <h2>{{localJobTitle}}</h2>
        <h3>{{testGetters}}</h3>
        <div>
            <button @click="changeName">change to xiao99</button>
        </div>
    </div>
</template>

<script>
    import {mapActions, mapState, mapGetters} from 'vuex'
    export default {
        computed:{
            // userName:function(){
            //     return this.$store.state.Login.userName
            // }
            ...mapState({
                userName: state=>state.Login.userName
            }),

            ...mapGetters(['localJobTitle','testGetters'])
        },
        methods:{
            changeName:function(){
                this.$store.dispatch("changeName","xiao99")
            }
        }
    }
</script>