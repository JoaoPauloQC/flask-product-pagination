document.addEventListener("DOMContentLoaded",function(){

    let paged__overlay = document.querySelector(".paged__overlay")
    let loading = document.querySelector(".loading")
    console.log(loading)    
    let pagination__btns = document.querySelectorAll(".pagination__btn")
        console.log(pagination__btns)
        pagination__btns.forEach(btn => {
            btn.addEventListener("click",()=>{
                console.log(`I'm here and the page is ${paged__overlay} and btns are ${pagination__btns}`)
                paged__overlay.classList.remove("hidden")
                animateLoading()

            })


        })
        animateLoading = () =>{
            console.log("here")
            loading.style.transform = `rotate(0deg)`
            setInterval(()=>{
                rotateState = loading.style.transform.slice(7,8)
                console.log(rotateState)
                for(i=8;i< loading.style.transform.length;i++){
                    if(parseInt(loading.style.transform[i]) == NaN){
                        break
                    }
                    rotateState = loading.style.transform.slice(7,i)
                }
                
                rotateState = parseInt(rotateState)
                loading.style.transform = `rotate(${rotateState+1}deg)`
                console.log(`Now ${loading.style.transform}`)
            },5)
        }
})
