pipeline {
    agent none

    stages {
        stage('Lint') {
            stages {
                stage('RPM Lint') {
                    agent {
                        dockerfile {
                            filename 'Dockerfile.centos:7'
                            label 'docker_runner'
                            additionalBuildArgs  '--build-arg UID=$(id -u)'
                            args  '--group-add mock --cap-add=SYS_ADMIN --privileged=true'
                        }
                    }
                    steps {
                        sh 'make rpmlint'
                    }
                }
            }
        }
        stage('Build') {
            parallel {
                stage('Build on CentOS 7') {
                    agent {
                        dockerfile {
                            filename 'Dockerfile.centos:7'
                            label 'docker_runner'
                            additionalBuildArgs  '--build-arg UID=$(id -u)'
                            args  '--group-add mock --cap-add=SYS_ADMIN --privileged=true'
                        }
                    }
                    steps {
                        sh '''rm -rf artifacts/
                              mkdir -p artifacts/
                              if make srpm; then
                                  if make mockbuild; then
                                      cp -af /var/lib/mock/epel-7-x86_64/root/builddir/build/RPMS artifacts/
                                      cp -af _topdir/SRPMS artifacts/
                                      cd artifacts/
                                      createrepo .
                                  else
                                      rc=\${PIPESTATUS[0]}
                                      cp -af /var/lib/mock/epel-7-x86_64/result artifacts/
                                      cp -af _topdir/SRPMS artifacts/
                                      exit \$rc
                                  fi
                              else
                                  exit \${PIPESTATUS[0]}
                              fi'''
                    }
                    post {
                        always {
                            archiveArtifacts artifacts: 'artifacts/**'
                        }
                    }
                }
                stage('Build on Ubuntu 16.04') {
                    agent {
                        label 'docker_runner'
                    }
                    steps {
                        echo "Building on Ubuntu is not implemented for the moment"
                    }
                }
            }
        }
    }
}
