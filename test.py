from docutils import nodes
from docutils.parsers.rst import Directive
import yaml

class YAMLFrontMatter(Directive):
    has_content = True

    def run(self):
        data = yaml.safe_load('\n'.join(self.content))
        self.state.document.yaml_front_matter = data
        return []
