node{

    stage('git clone'){
        //check CODE
        git credentialsId: 'cb90e0a8-8c41-4c29-ab72-e4a562d1f880', url: 'http://10.10.16.10:81/root/chinaskillproject.git'
    }
    #登录gitlab
    stage('maven build'){
        sh '''/usr/local/maven/bin/mvn package -DskipTests -f /var/jenkins_home/workspace/ChinaskillProject'''
    }
    #打包项目  -DskipTests 只打包，不测试  这个参数很重要，不加直接崩
    stage('image build'){
        sh '''
              echo $BUILD_ID
              docker build -t 10.10.16.10/chinaskillproject/gateway:$BUILD_ID -f /var/jenkins_home/workspace/ChinaskillProject/gateway/Dockerfile  /var/jenkins_home/workspace/ChinaskillProject/gateway
              docker build -t 10.10.16.10/chinaskillproject/config:$BUILD_ID -f /var/jenkins_home/workspace/ChinaskillProject/config/Dockerfile  /var/jenkins_home/workspace/ChinaskillProject/config'''
    }
    #构建镜像
    stage('push image'){
        sh '''docker login 10.10.16.10 -u=admin -p=Harbor12345
            docker push 10.10.16.10/chinaskillproject/gateway:$BUILD_ID
            docker push 10.10.16.10/chinaskillproject/config:$BUILD_ID'''
    }
    #推送镜像
    stage('deploy Rancher'){
        //执行部署脚本
       sh 'sed -i "s/sqshq\\/piggymetrics-gateway/10.10.16.10\\/chinaskillproject\\/gateway:$BUILD_ID/g" /var/jenkins_home/workspace/ChinaskillProject/yaml/deployment/gateway-deployment.yaml'
       sh 'sed -i "s/sqshq\\/piggymetrics-config/10.10.16.10\\/chinaskillproject\\/config:$BUILD_ID/g" /var/jenkins_home/workspace/ChinaskillProject/yaml/deployment/config-deployment.yaml'
       #修改deployment.taml文件中的镜像名称，不然找不到镜像
       sh 'kubectl create ns springcloud'
       #创建命名空间
       sh 'kubectl apply -f /var/jenkins_home/workspace/ChinaskillProject/yaml/deployment/gateway-deployment.yaml --kubeconfig=/root/.kube/config'
       sh 'kubectl apply -f /var/jenkins_home/workspace/ChinaskillProject/yaml/deployment/config-deployment.yaml --kubeconfig=/root/.kube/config'
       #创建deployment,--kubeconfig=/root/.kube/config指定命令的密钥
       sh 'kubectl apply -f /var/jenkins_home/workspace/ChinaskillProject/yaml/svc/gateway-svc.yaml --kubeconfig=/root/.kube/config'
       sh 'kubectl apply -f /var/jenkins_home/workspace/ChinaskillProject/yaml/svc/config-svc.yaml --kubeconfig=/root/.kube/config'
       #创建service
    }

}