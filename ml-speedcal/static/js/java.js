let button = document.getElementById('mybutton');


button.onclick = async () => {
  let number = document.getElementById("text").value;

  let rank = document.getElementById("ranks").value;

  let form_data = new FormData();

  form_data.append('name', number);
  form_data.append('rank' , rank);

  const response = await fetch("/fu",
    {
      method: 'POST', 
      body: form_data
    }
  );
  const text = await response.text()

  let num = document.getElementById("base_speed").value = text
};

let speed = document.querySelectorAll('.select-speed');

for (let i = 0;i < speed.length;i++) {
  

  speed[i].onchange = async () => {

    let num = document.getElementById("base_speed").value

    let val = speed[i].value

    let form_data = new FormData();

    let id = i

    form_data.append('value' , val)
    form_data.append('base' , num)
    form_data.append('index' , id)

    const response = await fetch("/on",
      {
        method: 'POST', 
        body:form_data
      }
    );

    const text = await response.text()

    let update = document.getElementById('updated_speed').value = text
};};

let rank = document.getElementById('ranks')

rank.onchange = async () => {

  let form_data = new FormData();

  form_data.append('rank' , rank.value);

  const response = await fetch("/rank_onchange",
    {
      method: 'POST', 
      body: form_data
    }
  );
  const text = await response.text();

  
  let num = document.getElementById("base_speed").value = text;
};

let guardian = document.getElementById('gaurdian')

guardian.onchange = async () => {

  let num = document.getElementById("base_speed").value
  let form_data = new FormData();

  form_data.append('gaurdian' , guardian.value)
  form_data.append('base' , num)
  

  const response = await fetch('/gaurdian_onchange' ,
  {
    method:'POST',
    body:form_data

  });

  const text = await response.text();

  let update = document.getElementById('updated_speed').value = text
}


let button1 = document.getElementById('mybutton1')

button1.onclick = async () => {

  
  let number = document.getElementById("text").value = '';
  let num = document.getElementById("base_speed").value = ''
  let update = document.getElementById('updated_speed').value = ''

  let speed = document.querySelectorAll('.select-speed');

  for (let i = 0;i < speed.length;i++) {
    speed[i].selectedIndex = 1
    speed[i].value = 'None'
    speed[i].text = 'None'
  }


  /**
   let spd = document.getElementById('speed1').selectedIndex = 1
  let ts1 = document.getElementById('ts').selectedIndex = 1
  let ts2 = document.getElementById('ts2').selectedIndex = 1
  */
  
  let guardian = document.getElementById('gaurdian').selectedIndex = 1 

};