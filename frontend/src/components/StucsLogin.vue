<template>
    <div></div>
</template>

<script>
/* eslint-disable */
export default {
    created() {
        this.$http.post('userlogin_stucs_cb', this.$route.query).then((response) => {
            let res = JSON.parse(response.bodyText)
            if(res.status === 0) {
                window.sessionStorage.token = res.token
                window.sessionStorage.username = res.username
                window.sessionStorage.name = res.name
                window.sessionStorage.user_type = res.user_type
                this.$router.push({ path: '/home' })
            } else {
                alert(res.message)
                this.$router.push('/')
            }
        }).catch(function(response){
            console.log('Error')
        })
    }
}
</script>

