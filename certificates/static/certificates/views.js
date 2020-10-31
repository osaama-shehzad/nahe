document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#verified').style.display = 'none';
    document.querySelector('#fail').style.display = 'none';
    document.querySelector('#transcripts').style.display = 'none';
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    const csrftoken = getCookie('csrftoken');

    document.querySelector('#search').onsubmit = () => {
        
        const request = new Request(
            '/search',
            {headers: {'X-CSRFToken': csrftoken}}
        );
        const cnic =  document.querySelector('#cnicfield').value;
        console.log (cnic);
        fetch(request, {
            method: 'POST', 
            body: JSON.stringify({
                cnic: cnic,
            })
        })
        .then(response => response.json())
        .then(result => {           
            if (!result['error']){
                data = JSON.parse(result);
                data.forEach (fellow => {
                    console.log(fellow);
                    var name = fellow.fields.name;
                    const ID = fellow.fields.ID; 
                    const date = fellow.fields.program; 
                    const CNIC = fellow.fields.CNIC; 
                    const graduation = fellow.fields.graduation;
                    if (!name.includes("Dr. ")){
                        name = "Dr. ".concat(name); 
                    }

                    document.querySelector('#download').addEventListener('click', () => {
                        fetch(`download/${date}/${name}/${graduation}/${ID}`);
                        alert('The certificate is downloaded in the current directory');

                    });

                    document.querySelector('#transcript').addEventListener('click', () => {
                        
                        document.querySelector('#verified').style.display = 'none';
                        document.querySelector('#fail').style.display = 'none';
                        document.querySelector('#transcripts').style.display = 'block';
                        document.querySelector('#home').style.display = 'none';    
                        document.querySelector('#form2').onsubmit = () => {
                            
                            const name = document.querySelector('#t-name').value;
                            const org = document.querySelector('#organization').value;
                            const msg = document.querySelector('#message').value;
                            const title = document.querySelector('#title').value;
                            const email = document.querySelector('#email').value;
                            const request = new Request(
                                '/sendrequest',
                                {headers: {'X-CSRFToken': csrftoken}}
                            );
                            
                            fetch(request, {
                                method: 'POST', 
                                body: JSON.stringify({
                                    name: name,
                                    org: org, 
                                    msg: msg, 
                                    title: title, 
                                    email: email,
                                    cnic: CNIC
                                })
                            })
                            .then(response => response.json())
                            .then(result => {
                                if (result.status == 'success'){
                                    alert ("Success! An email has been sent successfully to yours and the administrator's address!");
                                    window.location.reload(true);


                                } else {
                                    alert("Fail! An automated email could not be sent due to server error.");
                                }
                                   
                            })
                            return false;
                        };
                    });


                    document.querySelector('#search-again').addEventListener('click', () => {
                        window.location.reload(true);
                    
                    });

                    document.querySelector('#home').style.display = 'none';
                    document.querySelector('#fail').style.display = 'none';
                    document.querySelector('#verified').style.display = 'block';
                    document.querySelector('#list-home').innerHTML = `${name}`;
                    document.querySelector('#list-profile').innerHTML = `${ID}`;
                    document.querySelector('#list-messages').innerHTML = `${date}`;
                    document.querySelector('#note').innerHTML = `<b>Graduated!&nbsp;</b> It is verified that ${name} (CNIC # ${CNIC}) has successfully completed NFDP training held during ${fellow.fields.program}.
                    To request the transcript or to verify the authenticity of the certificate, please e-mail 'nahe.support@hec.gov.pk'. The certificate ID is: ${ID}.`;

                })
 
            } else {
                document.querySelector('#fail').style.display = 'block';
                document.querySelector('#fail').innerHTML = result['error'];
            }
        });  
        return false;
    }
});



