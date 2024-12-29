 var firebaseConfig = {
    apiKey: "AIzaSyC7Dw_cb5GyYQHhJlP2LRpw0gKQUIbTwy4",
    authDomain: "cardmaker-fe054.firebaseapp.com",
    databaseURL: "https://cardmaker-fe054.firebaseio.com",
    projectId: "cardmaker-fe054",
    storageBucket: "cardmaker-fe054.appspot.com",
    messagingSenderId: "1087015971680",
    appId: "1:1087015971680:web:5f965eb0b8b7122e9b4c05",
    measurementId: "G-B78P1JBLW2"
  };

  if (!firebase.apps.length) {
 // Initialize Firebase
  firebase.initializeApp(firebaseConfig);
  console.log(firebase.auth ());
  firebase.analytics();
}
  firebase.auth().useDeviceLanguage();
  console.log(firebase);


$(function () {
    $('#submit_mobile').on('click', function () {

var mobile_number = document.getElementById("mobile_number");
var dialcode = document.getElementById("dialcode").value;
console.log(dialcode);
var phoneno = /^\d{10}$/;
if (dialcode === 'nil') {
           console.log('d');
          document.getElementById("checkdiv").innerHTML = "Please select Your Country";
      }
 else if(!mobile_number.checkValidity() )  {
      console.log('m');
    document.getElementById("checkdiv").innerHTML = mobile_number.validationMessage;



  }
  else if(mobile_number.value.match(phoneno))
  {
var mobile_no = document.getElementById("mobile_number").value;


 window.recaptchaVerifier = new firebase.auth.RecaptchaVerifier('mobile_number', {
  'size': 'invisible',
  'callback': function(response) {
    // reCAPTCHA solved, allow signInWithPhoneNumber.
      grecaptcha.reset(window.recaptchaWidgetId);
    onSignInSubmit();
  }
});
var phoneNumber = dialcode+document.getElementById("mobile_number").value;
{#alert(phoneNumber);#}
console.log(phoneNumber);
var appVerifier = window.recaptchaVerifier;
console.log(appVerifier);

firebase.auth().signInWithPhoneNumber(phoneNumber, appVerifier)
    .then(function (confirmationResult) {
      // SMS sent. Prompt user to type the code from the message, then sign the
         console.log('code sent');
         console.log(confirmationResult);
         $("#div_mobile").css('display','none');
         $("#label_mobile").css('display','none');
         $("#div_otp").css('display','block');
         $("#submit_mobile").css('display','none');
         $("#submit_otp").css('display','block');
      // user in with confirmationResult.confirm(code).
      window.confirmationResult = confirmationResult;
    }).catch(function (error) {
      // Error; SMS not sent
        document.getElementById("checkdiv").innerHTML = "Code not sent please check Number or Try again after sometime";

      console.log('code not sent');
      console.log(error);
    });
  $("#checkdiv").empty();




        {#$('#apndloader').append('<div class="loader"></div>');#}

 var user = "{{user}}";
        let mobile_number  = document.getElementById('mobile_number').value;
        let csrftoken = "{{ csrf_token }}";

        // var Status = $(this).val();

  }
    else{
        document.getElementById("checkdiv").innerHTML = "Please enter correct mobile number";
  }

    });
});

$(function () {
    $('#submit_otp').on('click', function () {
        var code = document.getElementById('mobile_otp').value;
        var mobile_number = document.getElementById('mobile_number').value;
confirmationResult.confirm(code).then(function (result) {
  // User signed in successfully.
  var user = result.user;
  console.log('verification success :'+user);
     $.ajax({
            url: '/users/home/',
            type:'POST',
            data: {
                mobile_number: mobile_number,
                code: code
            },
            headers: {
            // 'Content-type': 'application/json',
            'X-CSRFToken': csrftoken
        },
            dataType : 'json',

            success: function(data){
                $('.loader').remove();
            // alert(data.data)
            var myStatus = data.status;

            if (myStatus==200){
            	// alert('done');
window.location = "/";

            // window.location = "/logoutview/";
            }
            if (myStatus==201){
                alert("please check amount and username")
            }



        }
        });
  // ...
}).catch(function (error) {
   document.getElementById("checkdiv").innerHTML ="Please Enter correct OTP";
});
    });
});
