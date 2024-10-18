import unittest
from unittest.mock import patch, mock_open
import xml.etree.ElementTree as ET
import logging

class TestXMLProcessing(unittest.TestCase):

    def test_valid_xml_parsing(self):
        xml_content = '''<Order>
                            <OrderID>1234</OrderID>
                            <Customer>
                                <CustomerID>5678</CustomerID>
                                <Name>John Doe</Name>
                            </Customer>
                            <TotalAmount>100.00</TotalAmount>
                        </Order>'''
        tree = ET.ElementTree(ET.fromstring(xml_content))
        self.assertIsNotNone(tree.getroot().find('OrderID'))

    @patch('logging.warning')
    def test_unexpected_field_logging(self, mock_log_warning):
        xml_content = '''<Order>
                            <OrderID>1234</OrderID>
                            <Discount>50%</Discount>
                            <TotalAmount>100.00</TotalAmount>
                        </Order>'''
        tree = ET.ElementTree(ET.fromstring(xml_content))
        root = tree.getroot()

        EXPECTED_FIELDS = ['OrderID', 'Customer', 'Products', 'TotalAmount']
        for child in root:
            if child.tag not in EXPECTED_FIELDS:
                logging.warning(f"Unexpected field '{child.tag}'")

        mock_log_warning.assert_called_with("Unexpected field 'Discount'")

    def test_invalid_xml(self):
        xml_content = '''<Order>
                            <OrderID>1234
                            <Customer>John Doe</Customer>
                        </Order>'''  # Missing closing tags
        with self.assertRaises(ET.ParseError):
            ET.ElementTree(ET.fromstring(xml_content))

if __name__ == "__main__":
    unittest.main()
