import os
import hashlib
import json
import logging
from typing import Dict, Any, List, Optional
from jinja2 import Environment, FileSystemLoader, TemplateError
from client.transformer_agent import TransformerAgent


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TemplateManager:
    """Manages Jinja2 templates for data transformation with caching and validation"""
    
    def __init__(self, templates_dir: str = "templates"):
        """
        Initialize the TemplateManager.
        
        :param templates_dir: Directory to store and load templates
        """
        self.templates_dir = templates_dir
        self._ensure_templates_dir()
        
        # Initialize Jinja2 environment with better configuration
        self.env = Environment(
            loader=FileSystemLoader(templates_dir), 
            autoescape=True,
            trim_blocks=True,
            lstrip_blocks=True
        )
        
        # Cache for loaded templates
        self._template_cache: Dict[str, str] = {}
        
        logger.info(f"TemplateManager initialized with directory: {templates_dir}")
    
    def _ensure_templates_dir(self) -> None:
        """Ensure the templates directory exists."""
        if not os.path.exists(self.templates_dir):
            os.makedirs(self.templates_dir, exist_ok=True)
            logger.info(f"Created templates directory: {self.templates_dir}")
    
    def get_template_filename(self, api_url: str, output_schema: Dict[str, Any]) -> str:
        """
        Generate a unique template filename based on API URL and output schema.
        
        :param api_url: The API endpoint URL
        :param output_schema: The output schema dictionary
        :return: Unique filename for the template
        """
        # Create a more robust hash that includes both URL and schema
        content = f"{api_url}#{json.dumps(output_schema, sort_keys=True)}"
        hash_object = hashlib.sha256(content.encode())  # Use SHA256 for better collision resistance
        return f"transformer_{hash_object.hexdigest()[:16]}.j2"  # Use first 16 chars for readability
    
    def template_exists(self, api_url: str, output_schema: Dict[str, Any]) -> bool:
        """
        Check if a template exists for the given API and schema.
        
        :param api_url: The API endpoint URL
        :param output_schema: The output schema dictionary
        :return: True if template exists, False otherwise
        """
        template_filename = self.get_template_filename(api_url, output_schema)
        template_path = os.path.join(self.templates_dir, template_filename)
        exists = os.path.exists(template_path) and os.path.isfile(template_path)
        
        if exists:
            logger.debug(f"Template exists: {template_filename}")
        
        return exists
    
    def load_template(self, api_url: str, output_schema: Dict[str, Any]) -> str:
        """
        Load an existing template from disk.
        
        :param api_url: The API endpoint URL
        :param output_schema: The output schema dictionary
        :return: Template content as string
        :raises FileNotFoundError: If template doesn't exist
        :raises Exception: If template cannot be read
        """
        template_filename = self.get_template_filename(api_url, output_schema)
        
        # Check cache first
        if template_filename in self._template_cache:
            logger.debug(f"Loading template from cache: {template_filename}")
            return self._template_cache[template_filename]
        
        template_path = os.path.join(self.templates_dir, template_filename)
        
        if not os.path.exists(template_path):
            raise FileNotFoundError(f"Template not found: {template_path}")
        
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Cache the loaded template
            self._template_cache[template_filename] = content
            logger.info(f"Loaded template: {template_filename}")
            return content
            
        except Exception as e:
            raise Exception(f"Failed to read template {template_path}: {str(e)}")
    
    def save_template(self, api_url: str, output_schema: Dict[str, Any], transformer_content: str) -> str:
        """
        Save a template to the templates directory.
        
        :param api_url: The API endpoint URL
        :param output_schema: The output schema dictionary
        :param transformer_content: The Jinja2 template content
        :return: Path to the saved template file
        :raises Exception: If template cannot be saved
        """
        template_filename = self.get_template_filename(api_url, output_schema)
        template_path = os.path.join(self.templates_dir, template_filename)
        
        try:
            # Validate the template syntax before saving
            self.env.from_string(transformer_content)
            
            with open(template_path, 'w', encoding='utf-8') as f:
                f.write(transformer_content)
            
            # Update cache
            self._template_cache[template_filename] = transformer_content
            logger.info(f"Saved template: {template_filename}")
            return template_path
            
        except TemplateError as e:
            raise Exception(f"Invalid Jinja2 template syntax: {str(e)}")
        except Exception as e:
            raise Exception(f"Failed to save template {template_path}: {str(e)}")
    
    def get_or_create_template(self, 
                             api_url: str, 
                             input_data: Dict[str, Any], 
                             output_schema: Dict[str, Any], 
                             agent_config: Dict[str, Any]) -> str:
        """
        Load existing template or create new one using the transformer agent.
        
        :param api_url: The API endpoint URL
        :param input_data: Sample input data
        :param output_schema: The output schema dictionary
        :param agent_config: Configuration for the TransformerAgent
        :return: Jinja2 template content
        :raises Exception: If template cannot be loaded or created
        """
        template_filename = self.get_template_filename(api_url, output_schema)
        
        if self.template_exists(api_url, output_schema):
            logger.info(f"Loading existing template: {template_filename}")
            return self.load_template(api_url, output_schema)
        else:
            logger.info(f"Creating new template: {template_filename}")
            
            try:
                # Create agent and generate transformer
                agent = TransformerAgent(**agent_config)
                transformer = agent.generate_transformer(
                    input_schema=input_data,
                    output_schema=output_schema
                )
                
                # Save the template for future use
                template_path = self.save_template(api_url, output_schema, transformer)
                logger.info(f"Template saved to: {template_path}")
                
                # Log performance stats
                stats = agent.get_performance_stats()
                logger.info(f"Agent performance - Requests: {stats['total_requests']}, "
                          f"Avg response time: {stats['average_response_time']:.2f}s")
                
                return transformer
                
            except Exception as e:
                logger.error(f"Failed to create template: {str(e)}")
                raise
    
    def render_template(self, transformer_content: str, input_data: Dict[str, Any]) -> str:
        """
        Render a template with the given input data.
        
        :param transformer_content: The Jinja2 template content
        :param input_data: Data to render the template with
        :return: Rendered output as string
        :raises Exception: If template rendering fails
        """
        try:
            template = self.env.from_string(transformer_content)
            result = template.render(input_data=input_data)
            logger.debug("Template rendered successfully")
            return result
            
        except TemplateError as e:
            raise Exception(f"Template rendering error: {str(e)}")
        except Exception as e:
            raise Exception(f"Failed to render template: {str(e)}")
    
    def validate_template(self, transformer_content: str, sample_data: Optional[Dict[str, Any]] = None) -> bool:
        """
        Validate a template's syntax and optionally test with sample data.
        
        :param transformer_content: The Jinja2 template content
        :param sample_data: Optional sample data to test rendering
        :return: True if valid, False otherwise
        """
        try:
            template = self.env.from_string(transformer_content)
            
            if sample_data:
                template.render(input_data=sample_data)
            
            return True
            
        except (TemplateError, Exception) as e:
            logger.warning(f"Template validation failed: {str(e)}")
            return False
    
    def list_templates(self) -> List[str]:
        """
        List all available templates.
        
        :return: List of template filenames
        """
        if not os.path.exists(self.templates_dir):
            return []
        
        templates = []
        try:
            for filename in os.listdir(self.templates_dir):
                if filename.endswith('.j2'):
                    templates.append(filename)
        except Exception as e:
            logger.error(f"Failed to list templates: {str(e)}")
            return []
        
        return sorted(templates)
    
    def get_template_info(self, template_filename: str) -> Optional[Dict[str, Any]]:
        """
        Get information about a specific template.
        
        :param template_filename: Name of the template file
        :return: Dictionary with template information or None if not found
        """
        template_path = os.path.join(self.templates_dir, template_filename)
        
        if not os.path.exists(template_path):
            return None
        
        try:
            stat = os.stat(template_path)
            with open(template_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return {
                "filename": template_filename,
                "path": template_path,
                "size": stat.st_size,
                "modified": stat.st_mtime,
                "line_count": len(content.splitlines()),
                "is_valid": self.validate_template(content)
            }
            
        except Exception as e:
            logger.error(f"Failed to get template info for {template_filename}: {str(e)}")
            return None
    
    def delete_template(self, api_url: str, output_schema: Dict[str, Any]) -> bool:
        """
        Delete a specific template.
        
        :param api_url: The API endpoint URL
        :param output_schema: The output schema dictionary
        :return: True if deleted successfully, False otherwise
        """
        template_filename = self.get_template_filename(api_url, output_schema)
        template_path = os.path.join(self.templates_dir, template_filename)
        
        try:
            if os.path.exists(template_path):
                os.remove(template_path)
                # Remove from cache
                self._template_cache.pop(template_filename, None)
                logger.info(f"Deleted template: {template_filename}")
                return True
        except Exception as e:
            logger.error(f"Failed to delete template {template_filename}: {str(e)}")
        
        return False
    
    def clear_cache(self) -> None:
        """Clear the template cache."""
        self._template_cache.clear()
        logger.info("Template cache cleared")
