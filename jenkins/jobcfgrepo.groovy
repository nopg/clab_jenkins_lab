pipelineJob("cfg-repo-builder") {
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
                                pollSCM('* * * * *')
                            }
                            stages {
                                stage('git checkout') {
                                    steps {
                                        checkout([
                                            \$class: 'gitSCM',
                                            branches: [[name: '*/main']],
                                            extensions: [],
                                            userRemoteConfigs: [[
                                                credentialsId: '7b4834fd-ed61-47d4-9d79-a0caac9f2df9',
                                                url: 'https://github.com/nopg/temp-cfgrepo.git',
                                            ]]
                                        ])
                                    }
                                }
                                stage('load configs') {
                                    steps {
                                        echo 'loading all config files found to respective devices'
                                        // run the container on the same rgclab network so it can resolve the network devices!
                                        // see dockerfile for more info on why sudo... its a demo, let it slide :)
                                        sh 'sudo docker run --network rgclab demo-container:latest cfg_repo_builder.py load'
                                    }
                                }
                            }
                            post {
                                always {
                                    echo 'config files loaded successfully'
                                }
                            }
                        }""")
            }
        }
}
