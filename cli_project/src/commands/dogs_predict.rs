


mod private
{
  use reqwest::blocking::Client;
  use crate::commands::dogs::ScriptResponse;

  pub fn command() 
  {
    let client = Client::new();

    let response = client
    .post( "http://dogs-ml:5000/predict" )
    .send()
    .expect( "Failed to send request" );

    if response.status().is_success() 
    {
      let script_response : ScriptResponse = response.json().unwrap();
      match script_response.status.as_str() 
      {
        "success" => println!( "Success:\n{}", script_response.output.unwrap_or_default() ),
        "error" => eprintln!( "Error:\n{}", script_response.error.unwrap_or_default() ),
        _ => eprintln!( "Unexpected response" ),
      }
    } 
    else 
    {
      eprintln!( "HTTP Error: {}", response.status() );
    }
  }
}

pub use private::command;