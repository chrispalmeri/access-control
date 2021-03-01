Vagrant.configure("2") do |config|
    config.vm.define "door-control" do |controller|
        controller.vm.provider :virtualbox do |vb|
            vb.name = "door-control"
        end
        controller.vm.box = "bento/debian-10.8"
        controller.vm.network "forwarded_port", guest: 80, host: 8080
        controller.vm.provision "shell", path: "./install.sh", args: ["/vagrant"]
    end
end
