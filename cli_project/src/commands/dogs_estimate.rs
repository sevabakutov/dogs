

mod private
{
  use std::time::Duration;
  use clap::Parser;
  use reqwest::blocking::Client;
  use serde::Serialize;
  use crate::commands::dogs::ScriptResponse;

  #[ derive( Debug, Parser, Serialize ) ]
  pub struct Args
  {
    #[ arg( long ) ]
    pub dist : String,

    #[ arg( long ) ]
    pub start_train : String,

    #[ arg( long ) ]
    pub end_train : String,

    #[ arg( long ) ]
    pub start_test : String,

    #[ arg( long ) ]
    pub end_test : String,

    #[ arg( long ) ]
    pub grade : String,
  }

  pub fn command
  (
    args : Args
  )
  {
    let client = Client::builder()
    .timeout( Duration::from_secs( 5 * 24 * 60 * 60 ) ) // 5 days
    .build()
    .expect( "Failed to build client" );

    let response = client
    .post( "http://dogs-ml:5000/estimate" )
    .json( &args )
    .send()
    .expect( "Failed to send request" );

    if response.status().is_success() 
    {
      let script_response : ScriptResponse = response.json().unwrap();
      match script_response.status.as_str() 
      {
        "success" => 
        {
          println!( "Success:\n{}", script_response.output.unwrap_or_default() );
        }
        "error" => 
        {
          eprintln!( "Error:\n{}", script_response.error.unwrap_or_default() );
        }
        _ => 
        {
          eprintln!( "Unexpected response" );
        }
      }
    } 
    else 
    {
      eprintln!( "HTTP Error: {}", response.status() );
    }
  }

}

pub use private::
{
  Args,
  command,
};