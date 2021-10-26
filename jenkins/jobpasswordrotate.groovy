pipelineJob("password-rotate") {
	description()
	keepDependencies(false)
    disabled(false)
	definition {
		cps {
            // sandbox seems to let us bypass the script approval -- guessing we are just not
            // using anything that is not allowed in sandbox?
            sandbox(true)
script("""pipeline {
    agent any
    triggers {
        cron('0 * * * *')
    }
    stages {
        stage('update carls password') {
            steps {
                echo 'launching password rotate container'
                // run the container on the same clab network so it can resolve vault and the network devices!
                // see dockerfile for more info on why sudo... its a demo, let it slide :)
                sh 'sudo docker run --network clab demo-container:latest password_rotate.py'
            }
        }
    }
    post {
        always {
            echo 'password update complete'
        }
    }
}""")		
            }
	   }
}
