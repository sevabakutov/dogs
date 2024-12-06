


mod private
{
  use std::
  {
    path::Path,
    process::Command,
  };

  pub fn command()
  {
    let working_dir = Path::new( "C:\\projects\\git\\dogs" );
    let executable = "python";
    let script_path = Path::new( "C:\\projects\\git\\dogs\\scripts\\predict.py" );
    let script_args = vec![ "predict" ];

    println!( "{:?}", script_path );
    println!( "{:?}", script_args );

    let process = Command::new( executable )
    .current_dir( working_dir )
    .arg( script_path )
    .args( &script_args )
    .output()
    .expect( "Failed to execute process" );

    if process.status.success()
    {
      println!( "Success!" );
    }
    else 
    {
      eprintln!( "Error\n{}", String::from_utf8_lossy( &process.stderr ) );
    }
  }
}

pub use private::command;