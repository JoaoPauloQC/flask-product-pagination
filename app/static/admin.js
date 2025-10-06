document.addEventListener("DOMContentLoaded",function(){

    let form = document.getElementById("newproduct__form")
    form.addEventListener("submit",(e)=>{
        e.preventDefault()
        let name = document.getElementById("name").value
        let price = document.getElementById("price").value
        console.log(name + " " + price)
        fetch("/api/newproduct",{
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
              },
            body: JSON.stringify({
                nome: name,
                preco: price
            })


        }).then(res=> res.json()).then(data=> console.log(data.Status))

    })

    let exclude_btns = document.querySelectorAll(".exclude__btn")
    exclude_btns.forEach(btn =>{

        btn.addEventListener("clihttp://127.0.0.1:5000/paged?page=2ck",function(e){
            e.preventDefault()
            console.log(this.id)
            id = (this.id).split("-")[1]
            console.log(id)
            fetch(`/api/exclude/${id}`).then(res => res.json()).then(data=> console.log(data.status) )
        })

    })


})