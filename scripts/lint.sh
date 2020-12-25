isort -c whattodo tests -c --diff \
&& black --check --diff whattodo tests \
&& pylint-fail-under --fail_under 9.0 whattodo/ \
&& mypy whattodo tests