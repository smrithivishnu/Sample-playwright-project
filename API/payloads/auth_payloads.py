import uuid
import random
import string
from datetime import datetime, timedelta
from Utilities.excel_reader import get_random_port, read_port_list_excel
from Utilities.test_data_manager import TestDataManager

class AuthPayloads:

    @staticmethod
    def get_port_function(port_index=0):
        """
        Get port function for a specific port index
        First port gets 'C', others get random from available functions except 'C'
        """
        test_data = TestDataManager.get_test_data()
        port_functions = test_data['port_functions']
        
        if port_index == 0:
            # First port always gets 'C'
            return port_functions['first_port_function']
        else:
            # Other ports get random function from available list except 'C'
            available_functions = port_functions['available_functions']
            # Remove 'C' from list for other ports
            other_functions = [func for func in available_functions if func != 'C']
            return random.choice(other_functions)

    @staticmethod
    def get_multiple_random_ports(count=5):
        """
        Get multiple random ports from Excel file without duplicates
        Returns list of port data dictionaries
        """
        import time
        
        all_ports = read_port_list_excel()
        if len(all_ports) < count:
            count = len(all_ports)
        
        # Debug: Print available ports and selection info
        print(f"DEBUG: Available ports: {len(all_ports)}")
        print(f"DEBUG: Requested ports: {count}")
        
        # Ensure we have enough different ports
        if len(all_ports) < count:
            count = len(all_ports)
        
        # Shuffle the ports list to ensure randomness
        random.shuffle(all_ports)
        
        # Take the first 'count' ports after shuffling
        selected_ports = all_ports[:count]
        
        # Debug: Print selected ports
        print(f"DEBUG: Actually selected ports:")
        for i, port in enumerate(selected_ports):
            print(f"  Selected {i+1}: {port['VIP_EXT_REF']} - {port['VIP_PORT_NAME']}")
        
        return selected_ports

    @staticmethod
    def get_arrival_departure_status(port_index=0, ar_position=None):
        """
        Get arrival/departure status based on port index and logic
        Returns appropriate status based on position in voyage
        SA can be many, only one AR, .. can be many
        Before AR only SA will be there, after AR only .. will be there
        """
        # If no AR position specified, use position 2 for consistent sequence
        if ar_position is None:
            ar_position = 2  # Fixed position for AR (3rd port: index 2)
        
        if port_index == ar_position:
            # This is the one AR port
            return 'AR'
        elif port_index < ar_position:
            # Ports before AR are SA (Sailed) - can be many
            return 'SA'
        else:
            # Ports after AR are .. (Scheduled) - can be many
            return '..'

    @staticmethod
    def generate_port_block(imo_no, vsl_name, vsl_code, voyage_no, voyage_status, port_data, port_order=100, arrival_local=None, departure_local=None, arrival_departure_status=None):
        """
        Generate a single port block for voyage itinerary
        """
        # Calculate port index based on port_order (100, 200, 300...) -> (0, 1, 2...)
        port_index = (port_order // 100) - 1
        # Get port function based on port index (first port gets 'C', others random except 'C')
        port_function = AuthPayloads.get_port_function(port_index)
        
        # Generate unique PK_HASH using voyage number and port order
        pk_hash = f"{voyage_no}{port_order}"
        
        # Generate estimate ID using voyage number and random number
        estimate_id = f"{voyage_no}{2026}"
        
        # Get email data from test_data.json
        test_data = TestDataManager.get_test_data()
        email_data = test_data['email_data']
        
        # Use provided arrival_departure_status or get based on port index logic
        if arrival_departure_status is None:
            arrival_departure_status = AuthPayloads.get_arrival_departure_status(port_index)
        
        # Use provided dates or default to current date/time
        if arrival_local is None:
            arrival_local = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        if departure_local is None:
            departure_local = (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%dT%H:%M:%S")
        
        return {
            "IMO_NO": imo_no,
            "VIP_VSL_NAME": vsl_name,
            "VIP_VSL_CODE": vsl_code,
            "VIP_VOYAGE_NO": voyage_no,
            "VIP_VOYAGE_STATUS": voyage_status,
            "VIP_TRADE_AREA_NAME": "727 EU.ASIA",
            "VIP_LOB_CODE": "EUR/ASA",
            "VIP_PORT_NO": 24801,
            "VIP_EXT_REF": port_data["VIP_EXT_REF"],
            "VIP_PORT_NAME": port_data["VIP_PORT_NAME"],
            "VIP_PORT_COUNTRY": port_data["VIP_PORT_COUNTRY"],
            "VIP_PORT_FUNC_DTL": port_function,
            "VIP_PORT_ORDER": port_order,
            "VIP_ARRIVAL_LOCAL": arrival_local,
            "VIP_DEPARTURE_LOCAL": departure_local,
            "VIP_IS_BUNKING_PORT": False,
            "VIP_ARRIVAL_DEPARTURE_STATUS": arrival_departure_status,
            "PK_HASH": pk_hash,
            "recordDel": False,
            "VIP_VOYAGE_EST_ID": estimate_id,
            "VIP_OPS_COORDINATOR_EMAIL": email_data["VIP_OPS_COORDINATOR_EMAIL"],
            "VIP_USER_GROUP_EMAIL": email_data["VIP_USER_GROUP_EMAIL"]
        }

    @staticmethod
    def create_payload_with_same_voyage_different_ports(imo_no, vsl_name, vsl_code, voyage_status, port_count=3):
        """
        Create payload with same voyage number but different ports
        """
        # Generate voyage number
        random_number = ''.join(random.choices(string.digits, k=8))
        voyage_no = f"{imo_no}{random_number}"
        
        # Get random ports
        selected_ports = AuthPayloads.get_multiple_random_ports(port_count)
        
        data_blocks = []
        current_date = datetime.now()
        departure_date = current_date
        
        for i, port_data in enumerate(selected_ports):
            port_order = (i + 1) * 100  # 100, 200, 300...
            port_function = AuthPayloads.get_port_function(i)
            
            # Calculate arrival date (15-30 days after current departure)
            inter_port_days = random.randint(15, 30)
            arrival_date = departure_date + timedelta(days=inter_port_days)
            
            # Calculate departure date (5-10 days after arrival)
            departure_date = arrival_date + timedelta(days=random.randint(5, 10))
            
            # Create port block
            port_block = AuthPayloads.generate_port_block(
                imo_no=imo_no,
                vsl_name=vsl_name,
                vsl_code=vsl_code,
                voyage_no=voyage_no,
                voyage_status=voyage_status,
                port_data=port_data,
                port_order=port_order,
                arrival_local=arrival_date.strftime("%Y-%m-%dT%H:%M:%S"),
                departure_local=departure_date.strftime("%Y-%m-%dT%H:%M:%S")
            )
            
            data_blocks.append(port_block)
            
            # Update departure date for next port calculation
            departure_date = departure_date
        
        return {
            "req_id": str(uuid.uuid4()),
            "isFullLoad": False,
            "data": data_blocks
        }

    @staticmethod
    def create_payload_with_same_voyage_same_ports(imo_no, vsl_name, vsl_code, voyage_status, port_count=3):
        """
        Create payload with same voyage number and same ports
        """
        # Generate voyage number
        random_number = ''.join(random.choices(string.digits, k=8))
        voyage_no = f"{imo_no}{random_number}"
        
        # Get single port and duplicate it
        single_port = AuthPayloads.get_multiple_random_ports(1)[0]
        
        data_blocks = []
        current_date = datetime.now()
        departure_date = current_date
        
        for i in range(port_count):
            port_order = (i + 1) * 100  # 100, 200, 300...
            port_function = AuthPayloads.get_port_function(i)
            
            # Calculate arrival date (15-30 days after current departure)
            inter_port_days = random.randint(15, 30)
            arrival_date = departure_date + timedelta(days=inter_port_days)
            
            # Calculate departure date (5-10 days after arrival)
            departure_date = arrival_date + timedelta(days=random.randint(5, 10))
            
            # Create port block (same port data for all)
            port_block = AuthPayloads.generate_port_block(
                imo_no=imo_no,
                vsl_name=vsl_name,
                vsl_code=vsl_code,
                voyage_no=voyage_no,
                voyage_status=voyage_status,
                port_data=single_port,
                port_order=port_order,
                arrival_local=arrival_date.strftime("%Y-%m-%dT%H:%M:%S"),
                departure_local=departure_date.strftime("%Y-%m-%dT%H:%M:%S")
            )
            
            data_blocks.append(port_block)
            
            # Update departure date for next port calculation
            departure_date = departure_date
        
        return {
            "req_id": str(uuid.uuid4()),
            "isFullLoad": False,
            "data": data_blocks
        }

    @staticmethod
    def create_basic_payload(imo_no, vsl_name, vsl_code, voyage_status, port_count=None):
        """
        Create a basic voyage itinerary payload with specified number of ports
        """
        # Get test data for vessel and email
        test_data = TestDataManager.get_test_data()
        vessel_data = test_data['vessel_data']
        email_data = test_data['email_data']
        
        # Use provided port_count or get from test_data.json
        if port_count is None:
            port_count = test_data['voyage_config']['port_count']
        
        # Get random ports
        selected_ports = AuthPayloads.get_multiple_random_ports(port_count)
        
        # Debug: Print selected ports to verify they're different
        print(f"DEBUG: Selected {len(selected_ports)} ports:")
        for i, port in enumerate(selected_ports):
            print(f"  Port {i+1}: {port['VIP_EXT_REF']} - {port['VIP_PORT_NAME']}")
        
        # Generate one AR position for the entire payload to ensure only one AR
        ar_position = random.randint(1, 3)  # Random position for AR (not first)
        
        # Generate voyage number and estimate ID
        random_digits = ''.join(random.choices(string.digits, k=8))
        voyage_no = f"{imo_no}{random_digits}"
        estimate_id = f"{voyage_no}{2026}"

        data_blocks = []
        current_date = datetime.now()
        
        for i, port_data in enumerate(selected_ports):
            port_order = (i + 1) * 100  # 100, 200, 300...
            port_function = AuthPayloads.get_port_function(i)
            
            # Debug: Print port data being used for this port block
            print(f"DEBUG: Creating port block {i+1} with port data: {port_data['VIP_EXT_REF']} - {port_data['VIP_PORT_NAME']}")
            
            # Calculate dates (each port 5-10 days apart)
            if i == 0:
                arrival_date = current_date
                departure_date = current_date + timedelta(days=random.randint(5, 10))
            else:
                arrival_date = departure_date + timedelta(days=random.randint(2, 5))
                departure_date = arrival_date + timedelta(days=random.randint(5, 10))
            
            port_block = {
                "IMO_NO": imo_no,
                "VIP_VSL_NAME": vsl_name,
                "VIP_VSL_CODE": vsl_code,
                "VIP_VOYAGE_NO": voyage_no,
                "VIP_VOYAGE_STATUS": voyage_status,
                "VIP_TRADE_AREA_NAME": "727 EU.ASIA",
                "VIP_LOB_CODE": "EUR/ASA",
                "VIP_PORT_NO": 24801,
                "VIP_EXT_REF": port_data["VIP_EXT_REF"],
                "VIP_PORT_NAME": port_data["VIP_PORT_NAME"],
                "VIP_PORT_COUNTRY": port_data["VIP_PORT_COUNTRY"],
                "VIP_PORT_FUNC_DTL": port_function,
                "VIP_PORT_ORDER": port_order,
                "VIP_ARRIVAL_LOCAL": arrival_date.strftime("%Y-%m-%dT%H:%M:%S"),
                "VIP_DEPARTURE_LOCAL": departure_date.strftime("%Y-%m-%dT%H:%M:%S"),
                "VIP_IS_BUNKING_PORT": False,
                "VIP_ARRIVAL_DEPARTURE_STATUS": AuthPayloads.get_arrival_departure_status(i, ar_position),
                "PK_HASH": f"{voyage_no}{port_order}",
                "recordDel": False,
                "VIP_VOYAGE_EST_ID": estimate_id,
                "VIP_OPS_COORDINATOR_EMAIL": email_data["VIP_OPS_COORDINATOR_EMAIL"],
                "VIP_USER_GROUP_EMAIL": email_data["VIP_USER_GROUP_EMAIL"]
            }
            
            data_blocks.append(port_block)
        
        return {
            "req_id": str(uuid.uuid4()),
            "isFullLoad": False,
            "data": data_blocks
        }

    @staticmethod
    def voyage_itinerary_payload(imo_no, vsl_name, vsl_code, voyage_status, port_count=6):
        """
        Create complete voyage itinerary payload with specified number of ports
        """
        # Generate voyage number
        random_number = ''.join(random.choices(string.digits, k=8))
        voyage_no = f"{imo_no}{random_number}"

        # Get random ports
        selected_ports = AuthPayloads.get_multiple_random_ports(port_count)
        
        # Generate one AR position for the entire payload to ensure only one AR
        ar_position = random.randint(1, 4)  # Random position for AR (not first)
        
        data_blocks = []
        current_date = datetime.now()
        departure_date = current_date
        
        for i, port_data in enumerate(selected_ports):
            port_order = (i + 1) * 100  # 100, 200, 300...
            port_function = AuthPayloads.get_port_function(i)
            
            # Calculate arrival date (15-30 days after current departure)
            inter_port_days = random.randint(15, 30)
            arrival_date = departure_date + timedelta(days=inter_port_days)
            
            # Calculate departure date (5-10 days after arrival)
            departure_date = arrival_date + timedelta(days=random.randint(5, 10))
            
            # Create port block using same port data (for same ports logic)
            if i == 0:
                # First port - use original port data
                port_block = AuthPayloads.generate_port_block(
                    imo_no=imo_no,
                    vsl_name=vsl_name,
                    vsl_code=vsl_code,
                    voyage_no=voyage_no,
                    voyage_status=voyage_status,
                    port_data=port_data,
                    port_order=port_order,
                    arrival_local=arrival_date.strftime("%Y-%m-%dT%H:%M:%S"),
                    departure_local=departure_date.strftime("%Y-%m-%dT%H:%M:%S"),
                    arrival_departure_status=AuthPayloads.get_arrival_departure_status(i, ar_position)
                )
            else:
                # Other ports - use their own port data
                port_block = AuthPayloads.generate_port_block(
                    imo_no=imo_no,
                    vsl_name=vsl_name,
                    vsl_code=vsl_code,
                    voyage_no=voyage_no,
                    voyage_status=voyage_status,
                    port_data=port_data,  # Use each port's own data
                    port_order=port_order,
                    arrival_local=arrival_date.strftime("%Y-%m-%dT%H:%M:%S"),
                    departure_local=departure_date.strftime("%Y-%m-%dT%H:%M:%S"),
                    arrival_departure_status=AuthPayloads.get_arrival_departure_status(i, ar_position)
                )
            
            data_blocks.append(port_block)
            
            # Update departure date for next port calculation
            departure_date = departure_date
        
        return {
            "req_id": str(uuid.uuid4()),
            "isFullLoad": False,
            "data": data_blocks
        }

    @staticmethod
    def add_port_to_existing_payload(existing_payload, imo_no, vsl_name, vsl_code, voyage_status, port_order=None):
        """
        Add a new port to an existing voyage itinerary payload
        """
        if port_order is None:
            # Find the highest existing port order and add 100
            existing_orders = [port['VIP_PORT_ORDER'] for port in existing_payload['data']]
            port_order = max(existing_orders) + 100 if existing_orders else 100
        
        # Get a random port for the new port data
        new_port_data = AuthPayloads.get_multiple_random_ports(1)[0]
        
        # Find the last port to get its departure date for continuity
        sorted_ports = sorted(existing_payload['data'], key=lambda x: x['VIP_PORT_ORDER'])
        last_port = sorted_ports[-1] if sorted_ports else None
        
        # Calculate dates as continuation from last port
        if last_port and last_port['VIP_DEPARTURE_LOCAL']:
            last_departure = datetime.strptime(last_port['VIP_DEPARTURE_LOCAL'], '%Y-%m-%dT%H:%M:%S')
            # Add 2-5 days between last departure and new arrival
            arrival_date = last_departure + timedelta(days=random.randint(2, 5))
            # Add 5-10 days stay at port
            departure_date = arrival_date + timedelta(days=random.randint(5, 10))
        else:
            # Fallback to current date if no last port found
            current_date = datetime.now()
            arrival_date = current_date + timedelta(days=random.randint(2, 5))
            departure_date = arrival_date + timedelta(days=random.randint(5, 10))
        
        # Create new port block using existing voyage details
        first_port = existing_payload['data'][0]
        new_port = AuthPayloads.generate_port_block(
            imo_no=imo_no,
            vsl_name=vsl_name,
            vsl_code=vsl_code,
            voyage_no=first_port['VIP_VOYAGE_NO'],
            voyage_status=voyage_status,
            port_data=new_port_data,
            port_order=port_order,
            arrival_local=arrival_date.strftime("%Y-%m-%dT%H:%M:%S"),
            departure_local=departure_date.strftime("%Y-%m-%dT%H:%M:%S")
        )
        
        # Create new payload with added port
        new_payload = existing_payload.copy()
        new_payload['data'].append(new_port)
        new_payload['req_id'] = str(uuid.uuid4())
        
        return new_payload

    @staticmethod
    def create_payload_with_same_voyage_different_ports(existing_payload, imo_no, vsl_name, vsl_code, voyage_status, port_count=1):
        """
        Create a new payload with same voyage details but different ports
        """
        # Get voyage details from existing payload
        first_port = existing_payload['data'][0]
        voyage_no = first_port['VIP_VOYAGE_NO']
        voyage_est_id = first_port['VIP_VOYAGE_EST_ID']
        
        # Get random ports
        new_ports = AuthPayloads.get_multiple_random_ports(port_count)
        
        # Find the highest existing port order and get the last port's status
        existing_orders = [port['VIP_PORT_ORDER'] for port in existing_payload['data']]
        max_order = max(existing_orders) if existing_orders else 0
        
        # Sort existing ports by order to find the last port
        sorted_ports = sorted(existing_payload['data'], key=lambda x: x['VIP_PORT_ORDER'])
        last_port = sorted_ports[-1] if sorted_ports else None
        last_port_status = last_port['VIP_ARRIVAL_DEPARTURE_STATUS'] if last_port else '..'
        
        # Determine the status for continuation ports based on the last port's status
        if last_port_status == 'AR':
            # If last port was AR, new ports should be '..' (Scheduled)
            continuation_status = '..'
        elif last_port_status == 'SA':
            # If last port was SA, we need to check if there's an AR before it
            # If no AR exists yet, the first new port should be AR
            has_ar = any(port['VIP_ARRIVAL_DEPARTURE_STATUS'] == 'AR' for port in existing_payload['data'])
            continuation_status = 'AR' if not has_ar else '..'
        else:
            # If last port was '..' (Scheduled), new ports should also be '..'
            continuation_status = '..'
        
        data_blocks = []
        
        # Find the last port to get its departure date for continuity
        sorted_ports = sorted(existing_payload['data'], key=lambda x: x['VIP_PORT_ORDER'])
        last_port = sorted_ports[-1] if sorted_ports else None
        
        # Initialize departure date from last port for continuity
        if last_port and last_port['VIP_DEPARTURE_LOCAL']:
            last_departure = datetime.strptime(last_port['VIP_DEPARTURE_LOCAL'], '%Y-%m-%dT%H:%M:%S')
            departure_date = last_departure
        else:
            # Fallback to current date if no last port found
            departure_date = datetime.now()
        
        for i, port_data in enumerate(new_ports):
            port_order = max_order + (i + 1) * 100  # Continue from existing max order
            
            # Calculate dates as continuation from previous port
            # Add 2-5 days between last departure and new arrival
            arrival_date = departure_date + timedelta(days=random.randint(2, 5))
            # Add 5-10 days stay at port
            departure_date = arrival_date + timedelta(days=random.randint(5, 10))
            
            # Create port block
            port_block = {
                "IMO_NO": imo_no,
                "VIP_VSL_NAME": vsl_name,
                "VIP_VSL_CODE": vsl_code,
                "VIP_VOYAGE_NO": voyage_no,  # Use same voyage number
                "VIP_VOYAGE_STATUS": voyage_status,
                "VIP_TRADE_AREA_NAME": "727 EU.ASIA",
                "VIP_LOB_CODE": "EUR/ASA",
                "VIP_PORT_NO": 24801,
                "VIP_EXT_REF": port_data["VIP_EXT_REF"],
                "VIP_PORT_NAME": port_data["VIP_PORT_NAME"],
                "VIP_PORT_COUNTRY": port_data["VIP_PORT_COUNTRY"],
                "VIP_PORT_FUNC_DTL": AuthPayloads.get_port_function(i),
                "VIP_PORT_ORDER": port_order,
                "VIP_ARRIVAL_LOCAL": arrival_date.strftime("%Y-%m-%dT%H:%M:%S"),
                "VIP_DEPARTURE_LOCAL": departure_date.strftime("%Y-%m-%dT%H:%M:%S"),
                "VIP_IS_BUNKING_PORT": False,
                "VIP_ARRIVAL_DEPARTURE_STATUS": continuation_status,
                "PK_HASH": f"{voyage_no}{port_order}",
                "recordDel": False,
                "VIP_VOYAGE_EST_ID": voyage_est_id,  # Use same estimate ID
                "VIP_OPS_COORDINATOR_EMAIL": first_port["VIP_OPS_COORDINATOR_EMAIL"],
                "VIP_USER_GROUP_EMAIL": first_port["VIP_USER_GROUP_EMAIL"]
            }
            
            data_blocks.append(port_block)
        
        return {
            "req_id": str(uuid.uuid4()),
            "isFullLoad": False,
            "data": data_blocks
        }

    @staticmethod
    def login_payload(username, password):
        """
        Create login payload for authentication
        """
        return {
            "username": username,
            "password": password
        }
