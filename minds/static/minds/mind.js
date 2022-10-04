
// read
function add(element)
{
    var list = element.parentElement.children[1].children;
    var sid = list[list.length - 2].value;
    // server
    fetch('checkList/'+sid, {
      })
      .then(response => response.json())
      .then(result => {
        check(list, result);
        console.log(result);
          
      });

    element.parentElement.children[1].style.display = "block";
}

function addToReadLists(element)
{
    list = element.parentElement.children;
    var checkList = checkedList(list, list.length - 2);
    var sid = list[list.length - 2].value;

    // server 
    fetch('addToReadlist/'+sid, {
        method: 'POST',
        body: JSON.stringify({
            checkList: checkList
        })
      })
      .then(response => response.json())
      .then(result => {
        if (result['message'] == "1")
        {
            element.parentElement.style.display = "none";
            // alert("hey");
            console.log(result);
        }
          
      });
}

function checkedList(checkboxes, len)
{
    var checked = []
    for (var i = 0; i < len; i++)
    {
        if (checkboxes[i].children[0].checked)
        {
            checked.push(checkboxes[i].children[0].value)
        }
    }
    return checked;
}

function check(list, result)
{
    for (var i = 0; i < list.length - 2; i++)
    {
        for (var j = 0; j < result.length; j++) 
        {
            if (list[i].children[0].value == result[j].title)
            {
                list[i].children[0].checked = true;
            }
        }
    } 
}


function createReadlist()
{
    var name = document.querySelector('#readlist-name').value;
    // server
    fetch('addReadList/'+name, {
    })
    .then(response => response.json())
    .then(result => {
        if (result['message'] == "1")
        {
            window.location.href = "../../showReadinglists"; 
        }
    });
}

// chats
function search(name){
    // send 
    fetch('/search/'+name)
    .then(response => response.json())
    .then(result => {
        document.querySelector('.list-group-chat').innerHTML="";
        const ulNode = document.createElement("ul");
        for (let i = 0; i < result.length; i++) {
            const aNode = document.createElement("a");
            aNode.href = `/chat/${result[i].id}`;
            const liNode = document.createElement("li");
            liNode.innerHTML = `${result[i].username} (${result[i].email})`
            aNode.appendChild(liNode);
            ulNode.appendChild(aNode);
            // document.querySelector('.list-group').innerHTML += `<a href="/chat/${result[i].id}" style="padding:10px;"><li>${result[i].username} (${result[i].email})</li></a>`;
        }
        document.querySelector('.list-group-chat').appendChild(ulNode);
        if(result['success']) {
            // alert(result['success']);
        }
    });
}

function chat(){
    const list = document.querySelector('.chating');
    list.removeChild(list.lastElementChild);
    list.removeChild(list.lastElementChild);
    list.removeChild(list.lastElementChild);
    message = document.querySelector('#chat-message').value;
    id = document.querySelector('#chat-id').value;
    // send 
    fetch('/send_message', {
        method: 'POST',
        body: JSON.stringify({
            message: message,
            id: id
        })
        })
        .then(response => response.json())
        .then(result => {
            console.log(result);
            if(result['error']) {
                document.querySelector('#send-error').innerHTML = `<div class="alert alert-danger" role="alert">${result['error']}</div>`;
            }
            if(result['message']) {
                const divNode = document.createElement("div");
                divNode.className = "left";
                divNode.innerHTML = result['message'].message;
                list.appendChild(divNode);
                list.innerHTML +="<br> <br> <br>";
                // list.appendChild(document.createElement("br"))
                // list.appendChild(document.createElement("br"))
                window.scrollTo(0, document.body.scrollHeight);
                document.querySelector('#chat-message').value = "";
            }
        });
    return false;
}

// search for user
function searchForUser(name)
{
    // send 
    fetch('/search/'+name)
    .then(response => response.json())
    .then(result => {
        document.querySelector('.list-group').innerHTML="";
        const ulNode = document.createElement("ul");
        for (let i = 0; i < result.length; i++) {
            const aNode = document.createElement("a");
            aNode.href = `/profile/${result[i].id}`;
            const liNode = document.createElement("li");
            liNode.innerHTML = `${result[i].username} (${result[i].email})`
            aNode.appendChild(liNode);
            ulNode.appendChild(aNode);
            // document.querySelector('.list-group').innerHTML += `<a href="/chat/${result[i].id}" style="padding:10px;"><li>${result[i].username} (${result[i].email})</li></a>`;
        }
        document.querySelector('.list-group').appendChild(ulNode);
        if(result['success']) {
            // alert(result['success']);
        }
    });
}

// notifications
function markread(e)
{
    // alert(e.dataset.id);
    var nid =  e.dataset.id;
    fetch('markread/'+nid)
    .then(response => response.json())
    .then(result => {
        if(result['message']) {
            // alert("hey");
        }
    });
}