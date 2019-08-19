/* eslint-disable */
export function checktoken(success, failure = () => {}) {
    if (window.sessionStorage.token != null) {
        this.$http.post('checktoken', {'token': window.sessionStorage.token }).then(response => {
            success()
        }).catch(failure())
    }
    else failure();
}
