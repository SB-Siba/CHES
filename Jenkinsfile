pipeline{
    agent any

    environment {
        pipeline_name = 'andarbahar'
        jenkins_dir = '/var/lib/jenkins/workspace/'
        ubuntu_user_name = 'ubuntu'


        ip_address = '54.210.167.182'
        domain_name = ''

        database_name = 'rummygame'
        postgres_password = 'root'

        django_project_name = 'project'
    }
    stages {
        // soft build : requirement.txt, collectstatic, migrate
        
        // stage('soft build'){
        //     steps  {
        //         sh "chmod +x cicd/soft_build/entrypoint.sh"
        //         sh "cicd/soft_build/./entrypoint.sh"
        //     }
        // }

        //--------------------------------------------------------------------------------------------------
        // hard build : to setup the project first time

        stage('Entrypoint'){
            steps  {
                sh "chmod +x cicd/hard_build/entrypoint.sh"
                sh "cicd/hard_build/./entrypoint.sh"
            }
        }

        stage('Deploy Secrets'){
            steps  {
                sh "chmod +x cicd/hard_build/secrects_deploy.sh"
                sh "cicd/hard_build/./secrects_deploy.sh"
            }
        }

        stage('Setup DataBase'){
            steps  {
                sh "chmod +x cicd/hard_build/database.sh"
                sh "cicd/hard_build/./database.sh"
            }
        }

        stage('Setup Gunicorn'){
            steps {
                sh "chmod +x cicd/hard_build/gunicorn.sh"
                sh "cicd/hard_build/./gunicorn.sh"

            }
        }


        stage('setup NGINX'){
            steps {
                sh "chmod +x cicd/hard_build/nginx.sh"
                sh "cicd/hard_build/./nginx.sh"
            }
        }

        stage('setup Celery'){
            steps {
                sh "chmod +x cicd/hard_build/celery.sh"
                sh "cicd/hard_build/./celery.sh"
            }
        }

        stage('Setup Daphne'){
            steps {
                sh "chmod +x cicd/hard_build/daphne.sh"
                sh "cicd/hard_build/./daphne.sh"

            }
        }

        stage('soft build'){
            steps  {
                sh "chmod +x cicd/soft_build/entrypoint.sh"
                sh "cicd/soft_build/./entrypoint.sh"
            }
        }

    }
}
