deploy:
	ansible-playbook ansible_playbook_deploy.yml -i ./ansible.cfg

run-docker:
	docker run -d -p 8001:8000 avlomus-quran
