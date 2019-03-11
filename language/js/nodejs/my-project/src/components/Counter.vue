<template>
    <div id="counter">
        Count is {{count}}
        <button @click="increment">+1</button>
        <button @click="decrement">-1</button>
    </div>
</template>
<script>
    import { mapGetters, mapActions } from 'vuex'
    export default {
    //    computed:{
    //         counter() {
    //             return this.$store.state.count
    //         }
    //    } ,
    //    computed:{
    //         counter() {
    //                     return this.
    //                 }
    //    },
        computed:{
            ...mapGetters([
                'count'
            ])
            ,
            watch:{
              count:function(newValue){
                  if (newValue){
                      
                  }
              }
            }
        },

        methods: mapActions([
            'increment',
            'decrement'
        ])
    }
</script>