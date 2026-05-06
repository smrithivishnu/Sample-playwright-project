import pytest
import allure
import uuid
import random
import string
from datetime import datetime, timedelta
from API.endpoints.auth_api import AuthAPI
from API.payloads.auth_payloads import AuthPayloads
from Utilities.test_data_manager import TestDataManager


@allure.feature("Voyage Itinerary API")
@allure.story("Voyage Management")
class TestVoyageItinerary:
    
    # Class variables to store shared data across test cases
    shared_payload = None
    test_case_3_payload = None
    test_case_2_payload = None
    test_case_4_payload = None
    test_case_full_payload = None
    test_case_full_payload_estimateId_null = None
    test_case_11_payload = None
    test_case_12_payload = None
    
    # Class variables for test data
    test_data = TestDataManager.get_test_data()
    base_url = test_data["common_info"]["Url"]
    mw_token = test_data["common_info"]["MwToken"]
    vessel_data = test_data["vessel_data"]
    imo = vessel_data["IMO_NO"]
    vesselname = vessel_data["VIP_VSL_NAME"]
    vesselcode = vessel_data["VIP_VSL_CODE"]
    voyagestatus = vessel_data["VIP_VOYAGE_STATUS"]

    # Define new vessel details from test_data.json
    new_imo_no = test_data["new_vessel_data"]["IMO_NO"]
    new_vsl_name = test_data["new_vessel_data"]["VIP_VSL_NAME"]
    new_vsl_code = test_data["new_vessel_data"]["VIP_VSL_CODE"]
    
    # Initialize AuthAPI with common base URL
    auth_api = AuthAPI(base_url)
        
    # Set middleware token for this specific API
    auth_api.set_middleware_token(mw_token)

    @pytest.fixture(scope="class")
    def setup_payload(self):
        """
        Setup method to create shared payload once for all test methods
        This runs once before all test methods in class
        """
        print("=== Setting up shared payload for all test cases ===")
        
        # Create and store shared payload
        TestVoyageItinerary.shared_payload = AuthPayloads.voyage_itinerary_payload(
            TestVoyageItinerary.imo, 
            TestVoyageItinerary.vesselname, 
            TestVoyageItinerary.vesselcode, 
            TestVoyageItinerary.voyagestatus
        )
          
        return TestVoyageItinerary.shared_payload

    @staticmethod
    def verify_api_response(response, test_name="API Test"):
        """
        Common function to verify API response structure and log results
        """
        # Assertions
        assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
        
        response_data = response.json()
        assert response_data is not None, "Response data should not be None"
        
        # Verify response structure
        if "success" in response_data:
            assert response_data["success"] == True, "API call should be successful"
        
        print(f"{test_name} Completed Successfully!")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        return response_data

    @allure.title("Test Voyage Itinerary API - Initial")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_voyage_itinerary_initial(self, setup_payload):
        """
        Test voyage itinerary API with valid payload
        """
        # Make API call with shared payload but with unique req_id
        # Create a copy of payload with a new request ID
        test_payload = setup_payload.copy()
        test_payload['req_id'] = str(uuid.uuid4())
        
        response = TestVoyageItinerary.auth_api.voyage_itinerary(
            TestVoyageItinerary.imo, 
            TestVoyageItinerary.vesselname, 
            TestVoyageItinerary.vesselcode, 
            TestVoyageItinerary.voyagestatus, 
            test_payload
        )
        
        # Use common verification function
        TestVoyageItinerary.verify_api_response(response, "Voyage Itinerary API Test - Initial call")

    @allure.title("Test Voyage Itinerary API - Add New Port With full itinerary")
    @allure.severity(allure.severity_level.NORMAL)
    def test_voyage_itinerary_add_new_port(self, setup_payload):
        """
        Test the voyage itinerary API by adding a new port to the existing payload full itinerary
        """
        # Add a new port to the existing payload
        updated_payload = AuthPayloads.add_port_to_existing_payload(
            setup_payload, 
            TestVoyageItinerary.imo, 
            TestVoyageItinerary.vesselname, 
            TestVoyageItinerary.vesselcode, 
            TestVoyageItinerary.voyagestatus
        )

        # Store the test case 2 payload
        TestVoyageItinerary.test_case_2_payload = updated_payload.copy()
         
        # Make API call with the updated payload (already has new req_id)
        response = TestVoyageItinerary.auth_api.voyage_itinerary(
            TestVoyageItinerary.imo, 
            TestVoyageItinerary.vesselname, 
            TestVoyageItinerary.vesselcode, 
            TestVoyageItinerary.voyagestatus, 
            updated_payload
        )
        
        # Use common verification function
        TestVoyageItinerary.verify_api_response(response, "Voyage Itinerary API Test with New Port Added")

    @allure.title("Test Voyage Itinerary API - Same Voyage Different Ports")
    @allure.severity(allure.severity_level.NORMAL)
    def test_voyage_itinerary_same_voyage_different_ports(self, setup_payload):
        """
        Test the voyage itinerary API by using the updated_payload from test case 2
        with same VIP_VOYAGE_NO and VIP_VOYAGE_EST_ID values but with different ports,
        incremented VIP_PORT_ORDER, and proper date calculations
        """
        # Create payload with same voyage data but different ports using updated_payload
        print("\nCreating payload with same voyage data but different ports (using updated_payload)...")
        new_payload = AuthPayloads.create_payload_with_same_voyage_different_ports(
            TestVoyageItinerary.test_case_2_payload.copy(), 
            TestVoyageItinerary.imo, 
            TestVoyageItinerary.vesselname, 
            TestVoyageItinerary.vesselcode, 
            TestVoyageItinerary.voyagestatus,
            port_count=1
        )
        
        # Since this is a continuation, change the port function to something appropriate
        # For continuation ports, we'll use 'M' instead of the default function
        if len(new_payload['data']) > 0:
            original_function = new_payload['data'][0]['VIP_PORT_FUNC_DTL']
            new_payload['data'][0]['VIP_PORT_FUNC_DTL'] = 'M'  # Stop function for continuation
        
        # Store the test case 3 payload
        TestVoyageItinerary.test_case_3_payload = new_payload.copy()

        # Make API call with the new payload
        response = TestVoyageItinerary.auth_api.voyage_itinerary(
            TestVoyageItinerary.imo, 
            TestVoyageItinerary.vesselname, 
            TestVoyageItinerary.vesselcode, 
            TestVoyageItinerary.voyagestatus, 
            new_payload
        )
        
        # Use common verification function
        TestVoyageItinerary.verify_api_response(response, "Voyage Itinerary API Test with Same Voyage Different Ports")

    @allure.title("Test Voyage Itinerary API - Record Delete")
    @allure.severity(allure.severity_level.NORMAL)
    def test_voyage_itinerary_record_delete(self, setup_payload):
        """
        Test the voyage itinerary API by using the exact same data from test case 3
        but setting recordDel: true
        """
        # Copy the exact same data from test case 3 but change only recordDel to true
        record_delete_payload = TestVoyageItinerary.test_case_3_payload.copy()
        
        # Set recordDel: true for the exact same port data from test case 3
        print("Setting recordDel: true for the exact same port data from test case 3...")
        for port_block in record_delete_payload['data']:
            port_block['recordDel'] = True
           
        # Generate a new request ID for this test
        record_delete_payload['req_id'] = str(uuid.uuid4())

        # Store the test case 4 payload
        TestVoyageItinerary.test_case_4_payload = record_delete_payload.copy()
         
        # Make API call with the exact same payload but recordDel: true
        response = TestVoyageItinerary.auth_api.voyage_itinerary(
            TestVoyageItinerary.imo, 
            TestVoyageItinerary.vesselname, 
            TestVoyageItinerary.vesselcode, 
            TestVoyageItinerary.voyagestatus, 
            record_delete_payload
        )
        
        # Use common verification function
        TestVoyageItinerary.verify_api_response(response, "Voyage Itinerary API Test with Record Delete")
      
    @allure.title("Test Voyage Itinerary API - Update First Port Arrival and Last Port Departure")
    @allure.severity(allure.severity_level.NORMAL)
    def test_voyage_itinerary_update_first_arrival_last_departure(self, setup_payload):
        """
        Test the voyage itinerary API by updating VIP_ARRIVAL_LOCAL of first port
        and VIP_DEPARTURE_LOCAL of last port block in combined payload of all test cases
        """
        # Step 1: Get original payload (Test Case 1)
        original_payload = setup_payload.copy()
        original_payload['data'] = [port.copy() for port in setup_payload['data']]
        
        # Step 2: Get updated payload (Test Case 2)
        test_case_2_payload = TestVoyageItinerary.test_case_2_payload.copy()
        
        # Step 3: Get test case 3 payload
        test_case_3_payload = TestVoyageItinerary.test_case_3_payload.copy()

        # Step 4: Get test case 4 payload
        test_case_4_payload = TestVoyageItinerary.test_case_4_payload.copy()
        
        # Step 5: Combine all port data
        combined_ports = []
        
        # Add ports from original payload
        for port_block in original_payload['data']:
            combined_ports.append(port_block.copy())
        
        # Add ports from updated payload (excluding duplicates)
        existing_port_orders = {port['VIP_PORT_ORDER'] for port in combined_ports}
        for port_block in test_case_2_payload['data']:
            if port_block['VIP_PORT_ORDER'] not in existing_port_orders:
                combined_ports.append(port_block.copy())
                existing_port_orders.add(port_block['VIP_PORT_ORDER'])
        
        # Add ports from test case 3 (excluding duplicates)
        for port_block in test_case_3_payload['data']:
            if port_block['VIP_PORT_ORDER'] not in existing_port_orders:
                combined_ports.append(port_block.copy())
                existing_port_orders.add(port_block['VIP_PORT_ORDER'])
        
        # Add ports from test case 4 (excluding duplicates)
        for port_block in test_case_4_payload['data']:
            if port_block['VIP_PORT_ORDER'] not in existing_port_orders:
                combined_ports.append(port_block.copy())
                existing_port_orders.add(port_block['VIP_PORT_ORDER'])
        
        # Sort ports by VIP_PORT_ORDER to identify first and last correctly
        combined_ports.sort(key=lambda x: x['VIP_PORT_ORDER'])
        
        if len(combined_ports) == 0:
            print("No ports available to update")
            return
        
        # Step 6: Filter out ports with recordDel: true FIRST
        filtered_ports = []
        ports_removed = []
        
        for port_block in combined_ports:
            if port_block.get('recordDel', False):
                ports_removed.append(port_block)
                print(f"Removed port: {port_block['VIP_PORT_NAME']} (Order: {port_block['VIP_PORT_ORDER']}) - recordDel: {port_block['recordDel']}")
            else:
                filtered_ports.append(port_block)
                print(f"Kept port: {port_block['VIP_PORT_NAME']} (Order: {port_block['VIP_PORT_ORDER']}) - recordDel: {port_block.get('recordDel', False)}")
        
        if len(filtered_ports) == 0:
            print("No ports available after filtering")
            return

        
        # Step 7: Update first port's VIP_ARRIVAL_LOCAL and last port's VIP_DEPARTURE_LOCAL on FILTERED ports
        first_port = filtered_ports[0]
        last_port = filtered_ports[-1]
        
        # Store original values for comparison
        original_first_arrival = first_port['VIP_ARRIVAL_LOCAL']
        original_last_departure = last_port['VIP_DEPARTURE_LOCAL']
        
        # Update first port arrival date (set to a past date within last month)
        from datetime import datetime, timedelta
        import random
        
        days_ago = random.randint(1, 30)
        original_first_arrival_date = datetime.strptime(original_first_arrival, '%Y-%m-%dT%H:%M:%S')
        new_arrival_date = original_first_arrival_date - timedelta(days=days_ago)
        new_arrival_str = new_arrival_date.strftime('%Y-%m-%dT%H:%M:%S')
        
        # Update last port departure date (set to a date after original first arrival)
        # Parse the original first arrival date to calculate departure
        original_last_departure_date = datetime.strptime(original_last_departure, '%Y-%m-%dT%H:%M:%S')
        days_after_arrival = random.randint(2, 5)
        new_departure_date = original_last_departure_date + timedelta(days=days_after_arrival)
        new_departure_str = new_departure_date.strftime('%Y-%m-%dT%H:%M:%S')
        
        # Apply updates to filtered ports
        first_port['VIP_ARRIVAL_LOCAL'] = new_arrival_str
        last_port['VIP_DEPARTURE_LOCAL'] = new_departure_str
        
        # Step 8: Create final payload with updated dates (filtered)
        final_payload = {
            "req_id": str(uuid.uuid4()),
            "isFullLoad": False,
            "data": filtered_ports
        }

         # Store the test case payload
        TestVoyageItinerary.test_case_full_payload = final_payload.copy()
        
        # Step 9: Verify the updates
        if len(filtered_ports) > 0:
            updated_first_port = final_payload['data'][0]
            updated_last_port = final_payload['data'][-1]
            
            print(f"First port arrival updated from '{original_first_arrival}' to '{updated_first_port['VIP_ARRIVAL_LOCAL']}'")
            print(f"Last port departure updated from '{original_last_departure}' to '{updated_last_port['VIP_DEPARTURE_LOCAL']}'")
        else:
            print("No ports available after filtering")
            return
        
        # Make API call with the updated payload
        response = TestVoyageItinerary.auth_api.voyage_itinerary(
            TestVoyageItinerary.imo, 
            TestVoyageItinerary.vesselname, 
            TestVoyageItinerary.vesselcode, 
            TestVoyageItinerary.voyagestatus, 
            final_payload
        )
        
        # Use common verification function
        TestVoyageItinerary.verify_api_response(response, "Voyage Itinerary API Test with First Port Arrival and Last Port Departure Updates")

    @allure.title("Test Voyage Itinerary API - Voyage Number edit")
    @allure.severity(allure.severity_level.NORMAL)
    def test_voyage_itinerary_voyage_number_edit(self, setup_payload):
        """
        Test the voyage itinerary API by creating a payload with voyage number update
        """
        test_payload = TestVoyageItinerary.test_case_full_payload.copy()
        test_payload['req_id'] = str(uuid.uuid4())
        random_number = ''.join(random.choices(string.digits, k=8))
        voyage_no = f"{TestVoyageItinerary.imo}{random_number}"

        for port_block in test_payload['data']:
            port_block['VIP_VOYAGE_NO'] = voyage_no
        
        response = TestVoyageItinerary.auth_api.voyage_itinerary(
            TestVoyageItinerary.imo, 
            TestVoyageItinerary.vesselname, 
            TestVoyageItinerary.vesselcode, 
            TestVoyageItinerary.voyagestatus,
            test_payload
        )
        
        # Use common verification function
        TestVoyageItinerary.verify_api_response(response, "Voyage Itinerary API Test with Different Voyage Number and Null Estimate ID")
        
    @allure.title("Test Voyage Itinerary API - Update Arrival and Departure for One Port After Voyage Number Edit")
    @allure.severity(allure.severity_level.NORMAL)
    def test_voyage_itinerary_update_arrival_departure_one_port(self, setup_payload):
        """
        Test the voyage itinerary API by updating VIP_ARRIVAL_LOCAL and VIP_DEPARTURE_LOCAL 
        for one port in the full payload after voyage number edit test case
        """
        # Get the full payload (after voyage number edit)
        test_payload = TestVoyageItinerary.test_case_full_payload.copy()
        test_payload['req_id'] = str(uuid.uuid4())
        
        if len(test_payload['data']) == 0:
            print("No ports available to update")
            return
        
        # Select the first port for updating arrival and departure times
        selected_port = test_payload['data'][2]
        port_name = selected_port['VIP_PORT_NAME']
        
        # Store original values for comparison
        original_arrival = selected_port['VIP_ARRIVAL_LOCAL']
        original_departure = selected_port['VIP_DEPARTURE_LOCAL']
        
        # Update arrival date (set to a past date within last 30 days)
        from datetime import datetime, timedelta
        import random
        
        days_ago_arrival = random.randint(1, 3)
        original_arrival_date = datetime.strptime(original_arrival, '%Y-%m-%dT%H:%M:%S')
        new_arrival_date = original_arrival_date - timedelta(days=days_ago_arrival)
        new_arrival_str = new_arrival_date.strftime('%Y-%m-%dT%H:%M:%S')
        
        # Update departure date (set to a date after the new arrival)
        original_departure_date = datetime.strptime(original_departure, '%Y-%m-%dT%H:%M:%S')
        days_after_arrival = random.randint(1, 3)
        new_departure_date = original_departure_date + timedelta(days=days_after_arrival)
        new_departure_str = new_departure_date.strftime('%Y-%m-%dT%H:%M:%S')
        
        # Apply updates to the selected port
        selected_port['VIP_ARRIVAL_LOCAL'] = new_arrival_str
        selected_port['VIP_DEPARTURE_LOCAL'] = new_departure_str
        
        print(f"Updated arrival and departure times for port: {port_name}")
        print(f"  Arrival: {original_arrival} -> {new_arrival_str}")
        print(f"  Departure: {original_departure} -> {new_departure_str}")
        
        # Create payload with only the updated port
        single_port_payload = {
            "req_id": str(uuid.uuid4()),
            "isFullLoad": False,
            "data": [selected_port]
        }
        
        # Make API call with the single updated port
        response = TestVoyageItinerary.auth_api.voyage_itinerary(
            TestVoyageItinerary.imo, 
            TestVoyageItinerary.vesselname, 
            TestVoyageItinerary.vesselcode, 
            TestVoyageItinerary.voyagestatus, 
            single_port_payload
        )
        
        # Use common verification function
        TestVoyageItinerary.verify_api_response(response, "Voyage Itinerary API Test - Update Arrival and Departure for One Port")
        
    @allure.title("Test Voyage Itinerary API - Update Port Order")
    @allure.severity(allure.severity_level.NORMAL)
    def test_voyage_itinerary_update_port_order(self, setup_payload):
        """
        Test voyage itinerary API by updating port order of existing ports in test_case_full_payload
        """
        # Get the full payload with all ports
        test_payload = TestVoyageItinerary.test_case_full_payload.copy()
        test_payload['req_id'] = str(uuid.uuid4())
        
        # Interchange port order for existing ports (swap first and last ports)
        if len(test_payload['data']) >= 2:
            # Get first and last ports
            first_port = test_payload['data'][1]
            last_port = test_payload['data'][-1]
            
            # Store original orders
            first_original_order = first_port['VIP_PORT_ORDER']
            last_original_order = last_port['VIP_PORT_ORDER']
            
            # Swap the port orders
            first_port['VIP_PORT_ORDER'] = last_original_order
            last_port['VIP_PORT_ORDER'] = first_original_order
            
            # Generate new PK_HASH values instead of reusing
            import random
            first_new_pk_hash = f"{first_port['VIP_VOYAGE_NO']}{random.randint(10000, 99999)}"
            last_new_pk_hash = f"{last_port['VIP_VOYAGE_NO']}{random.randint(10000, 99999)}"
            
            # Update PK_HASH with new values
            first_port['PK_HASH'] = first_new_pk_hash
            last_port['PK_HASH'] = last_new_pk_hash
            
            print(f"Swapped port orders with new PK_HASH:")
            print(f"  {first_port['VIP_PORT_NAME']}: order {first_original_order} -> {last_original_order}, PK_HASH: {first_new_pk_hash}")
            print(f"  {last_port['VIP_PORT_NAME']}: order {last_original_order} -> {first_original_order}, PK_HASH: {last_new_pk_hash}")
        else:
            print("Need at least 2 ports to interchange orders")
            return
        
        # Make API call with updated port order
        response = TestVoyageItinerary.auth_api.voyage_itinerary(
            TestVoyageItinerary.imo, 
            TestVoyageItinerary.vesselname, 
            TestVoyageItinerary.vesselcode, 
            TestVoyageItinerary.voyagestatus,
            test_payload
        )
        
        # Use common verification function
        TestVoyageItinerary.verify_api_response(response, "Voyage Itinerary API Test with Port order Update")

    @allure.title("Test Voyage Itinerary API - Update Status Values")
    @allure.severity(allure.severity_level.NORMAL)
    def test_voyage_itinerary_update_status_values(self, setup_payload):
        """
        Test the voyage itinerary API by updating VIP_VOYAGE_STATUS to 'Completed/Closed'
        and VIP_ARRIVAL_DEPARTURE_STATUS to 'SA' for all ports in combined data
        """
        combined_ports = TestVoyageItinerary.test_case_full_payload['data'].copy()
        # Step 5: Update status values for all ports
        updated_combined_ports = []
        
        for port_block in combined_ports:
            updated_port = port_block.copy()
            # Update status values
            updated_port['VIP_VOYAGE_STATUS'] = 'Completed/Closed'
            updated_port['VIP_ARRIVAL_DEPARTURE_STATUS'] = 'SA'
            updated_combined_ports.append(updated_port)
        
        # Step 7: Create final payload with updated status values (filtered)
        final_payload = {
            "req_id": str(uuid.uuid4()),
            "isFullLoad": False,
            "data": updated_combined_ports
        }
        
        # Make API call with the updated payload
        response = TestVoyageItinerary.auth_api.voyage_itinerary(
            TestVoyageItinerary.imo, 
            TestVoyageItinerary.vesselname, 
            TestVoyageItinerary.vesselcode, 
            TestVoyageItinerary.voyagestatus, 
            final_payload
        )
        
        # Use common verification function
        TestVoyageItinerary.verify_api_response(response, "Voyage Itinerary API Test with Status Values Update")
        
    @allure.title("Test Voyage Itinerary API - Update Status After Completed/Closed")
    @allure.severity(allure.severity_level.NORMAL)
    def test_voyage_itinerary_update_status_after_completed_closed(self, setup_payload):
        """
        Test the voyage itinerary API by updating VIP_VOYAGE_STATUS after it was set to Completed/Closed
        and updating VIP_ARRIVAL_DEPARTURE_STATUS to AR and SA where SA will always be before AR based on port order
        """
        # Get the full payload (same as used in the Completed/Closed test case)
        combined_ports = TestVoyageItinerary.test_case_full_payload['data'].copy()
        
        if len(combined_ports) < 2:
            print("Need at least 2 ports to set SA and AR status")
            return
        
        # Sort ports by VIP_PORT_ORDER to ensure correct order
        combined_ports.sort(key=lambda x: x['VIP_PORT_ORDER'])
        
        # Update status values for all ports
        updated_combined_ports = []
        
        for i, port_block in enumerate(combined_ports):
            updated_port = port_block.copy()
            # Update voyage status
            updated_port['VIP_VOYAGE_STATUS'] = 'Commenced'  # Change from Completed/Closed to Active
            
            # Set arrival/departure status based on port order
            if i == 0:
                # First port gets SA (Sailed/Arrived)
                updated_port['VIP_ARRIVAL_DEPARTURE_STATUS'] = 'SA'
                print(f"Port {i+1} ({updated_port['VIP_PORT_NAME']}): SA")
            elif i == 1:
                # Second port gets AR (Arrived)
                updated_port['VIP_ARRIVAL_DEPARTURE_STATUS'] = 'AR'
                print(f"Port {i+1} ({updated_port['VIP_PORT_NAME']}): AR")
            else:
                # Remaining ports keep original status or set to Scheduled
                updated_port['VIP_ARRIVAL_DEPARTURE_STATUS'] = '..'  # Scheduled
                print(f"Port {i+1} ({updated_port['VIP_PORT_NAME']}): .. (Scheduled)")
            
            updated_combined_ports.append(updated_port)
        
        # Create final payload with updated status values
        final_payload = {
            "req_id": str(uuid.uuid4()),
            "isFullLoad": False,
            "data": updated_combined_ports
        }
        
        # Make API call with the updated payload
        response = TestVoyageItinerary.auth_api.voyage_itinerary(
            TestVoyageItinerary.imo, 
            TestVoyageItinerary.vesselname, 
            TestVoyageItinerary.vesselcode, 
            TestVoyageItinerary.voyagestatus, 
            final_payload
        )
        
        # Use common verification function
        TestVoyageItinerary.verify_api_response(response, "Voyage Itinerary API Test - Update Status After Completed/Closed")
        
    @allure.title("Test Voyage Itinerary API - Different Voyage Number and Null Estimate ID")
    @allure.severity(allure.severity_level.NORMAL)
    def test_voyage_itinerary_different_voyage_null_estimate(self, setup_payload):
        """
        Test the voyage itinerary API by creating a payload with different voyage number
        and VIP_VOYAGE_EST_ID set to null
        """
        test_payload = setup_payload.copy()
        test_payload['req_id'] = str(uuid.uuid4())
        random_number = ''.join(random.choices(string.digits, k=8))
        voyage_no = f"{TestVoyageItinerary.imo}{random_number}"

        for port_block in test_payload['data']:
            port_block['VIP_VOYAGE_NO'] = voyage_no
            port_block['VIP_VOYAGE_EST_ID'] = None

        TestVoyageItinerary.test_case_full_payload_estimateId_null = test_payload.copy()
        
        response = TestVoyageItinerary.auth_api.voyage_itinerary(
            TestVoyageItinerary.imo, 
            TestVoyageItinerary.vesselname, 
            TestVoyageItinerary.vesselcode, 
            TestVoyageItinerary.voyagestatus,
            test_payload
        )
        
        # Use common verification function
        TestVoyageItinerary.verify_api_response(response, "Voyage Itinerary API Test with Voyage Number Edit")
        
    @allure.title("Test Voyage Itinerary API - Update Two Ports Status (AR->SA, Scheduled->AR) - No PK_HASH Change")
    @allure.severity(allure.severity_level.NORMAL)
    def test_voyage_itinerary_arrival_status_update(self, setup_payload):
        """
        Test voyage itinerary API by updating only 2 port blocks:
        1. Port with AR status -> SA
        2. Next port in order with Scheduled status -> AR
        """
        # Get the full payload with all ports
        test_payload = TestVoyageItinerary.test_case_full_payload_estimateId_null.copy()
        test_payload['req_id'] = str(uuid.uuid4())
        
        # Find ports to update
        ar_port = None
        scheduled_port = None
        ar_port_index = None
        
        # Look for first port with AR status
        for i, port_block in enumerate(test_payload['data']):
            if port_block.get('VIP_ARRIVAL_DEPARTURE_STATUS') == 'AR':
                ar_port = port_block.copy()
                ar_port['VIP_ARRIVAL_DEPARTURE_STATUS'] = 'SA'  # AR -> SA
                ar_port_index = i
                break
        
        # Look for next port with Scheduled status
        for i in range(len(test_payload['data'])):
            if test_payload['data'][i].get('VIP_ARRIVAL_DEPARTURE_STATUS') == '..' and i > ar_port_index:
                scheduled_port = test_payload['data'][i].copy()
                scheduled_port['VIP_ARRIVAL_DEPARTURE_STATUS'] = 'AR'  # Scheduled -> AR
                break
        
        if ar_port is None or scheduled_port is None:
            print("Could not find required ports (AR and Scheduled) to update")
            return
        
        # Update the test_case_full_payload_estimateId_null with the changes
        for i, port_block in enumerate(TestVoyageItinerary.test_case_full_payload_estimateId_null['data']):
            if i == ar_port_index:
                # Update AR port to SA
                TestVoyageItinerary.test_case_full_payload_estimateId_null['data'][i]['VIP_ARRIVAL_DEPARTURE_STATUS'] = 'SA'
                print(f"  Updated {port_block['VIP_PORT_NAME']} in test_case_full_payload_estimateId_null: AR -> SA")
            elif port_block.get('VIP_ARRIVAL_DEPARTURE_STATUS') == '..' and i > ar_port_index:
                # Update Scheduled port to AR
                TestVoyageItinerary.test_case_full_payload_estimateId_null['data'][i]['VIP_ARRIVAL_DEPARTURE_STATUS'] = 'AR'
                print(f"  Updated {port_block['VIP_PORT_NAME']} in test_case_full_payload_estimateId_null: .. -> AR")
                break
        
        # Create payload with only the 2 updated ports
        updated_ports = [ar_port, scheduled_port]
        
        print(f"Updated 2 ports (no PK_HASH change):")
        print(f"  {ar_port['VIP_PORT_NAME']}: AR -> SA")
        print(f"  {scheduled_port['VIP_PORT_NAME']}: Scheduled -> AR")
        
        # Create final payload with only the 2 updated ports
        final_payload = {
            "req_id": str(uuid.uuid4()),
            "isFullLoad": False,
            "data": updated_ports
        }
        
        # Make API call with only the 2 updated ports
        response = TestVoyageItinerary.auth_api.voyage_itinerary(
            TestVoyageItinerary.imo, 
            TestVoyageItinerary.vesselname, 
            TestVoyageItinerary.vesselcode, 
            TestVoyageItinerary.voyagestatus,
            final_payload
        )
        
        # Use common verification function
        TestVoyageItinerary.verify_api_response(response, "Voyage Itinerary API Test with Two Ports Status Update")

    @allure.title("Test Voyage Itinerary API - Same Voyage Add port - EstimateId null")
    @allure.severity(allure.severity_level.NORMAL)
    def test_voyage_itinerary_same_voyage_add_port_estimate_id_null(self, setup_payload):
        """
        Test the voyage itinerary API add new port with estimateId null
        """
        # Create payload with same voyage data but different ports using updated_payload
        new_payload = AuthPayloads.create_payload_with_same_voyage_different_ports(
            TestVoyageItinerary.test_case_full_payload_estimateId_null.copy(), 
            TestVoyageItinerary.imo, 
            TestVoyageItinerary.vesselname, 
            TestVoyageItinerary.vesselcode, 
            TestVoyageItinerary.voyagestatus,
            port_count=1
        )
        
        # Since this is a continuation, change the port function to something appropriate
        # For continuation ports, we'll use 'M' instead of the default function
        if len(new_payload['data']) > 0:
            original_function = new_payload['data'][0]['VIP_PORT_FUNC_DTL']
            new_payload['data'][0]['VIP_PORT_FUNC_DTL'] = 'M'  # Stop function for continuation
        
        # Store the test case 11 payload
        TestVoyageItinerary.test_case_11_payload = new_payload.copy()

        # Make API call with the new payload
        response = TestVoyageItinerary.auth_api.voyage_itinerary(
            TestVoyageItinerary.imo, 
            TestVoyageItinerary.vesselname, 
            TestVoyageItinerary.vesselcode, 
            TestVoyageItinerary.voyagestatus, 
            new_payload
        )
        
        # Use common verification function
        TestVoyageItinerary.verify_api_response(response, "Voyage Itinerary API Test with Same Voyage Add port EstimateId null")

    @allure.title("Test Voyage Itinerary API - Record Delete - EstimateId null")
    @allure.severity(allure.severity_level.NORMAL)
    def test_voyage_itinerary_record_delete_estimateId_null(self, setup_payload):
        """
        Test the voyage itinerary API by using the exact same data from test case 3
        but setting recordDel: true estimate id null
        """
        # Copy the exact same data from test case 3 but change only recordDel to true
        record_delete_payload = TestVoyageItinerary.test_case_11_payload.copy()
        
        # Set recordDel: true for the exact same port data from test case 3
        for port_block in record_delete_payload['data']:
            port_block['recordDel'] = True
           
        # Generate a new request ID for this test
        record_delete_payload['req_id'] = str(uuid.uuid4())

        # Store the test case 4 payload
        TestVoyageItinerary.test_case_12_payload = record_delete_payload.copy()
         
        # Make API call with the exact same payload but recordDel: true
        response = TestVoyageItinerary.auth_api.voyage_itinerary(
            TestVoyageItinerary.imo, 
            TestVoyageItinerary.vesselname, 
            TestVoyageItinerary.vesselcode, 
            TestVoyageItinerary.voyagestatus, 
            record_delete_payload
        )
        
        # Use common verification function
        TestVoyageItinerary.verify_api_response(response, "Voyage Itinerary API Test with Record Delete EstimateId null")
      
    @allure.title("Test Voyage Itinerary API - Update RecordDel to False After Record Delete")
    @allure.severity(allure.severity_level.NORMAL)
    def test_voyage_itinerary_update_record_del_false(self, setup_payload):
        """
        Test the voyage itinerary API by updating recordDel from true to false
        after the record delete test case
        """
        # Get the test_case_12_payload (which has recordDel: true)
        test_payload = TestVoyageItinerary.test_case_12_payload.copy()
        test_payload['req_id'] = str(uuid.uuid4())
        
        # Update recordDel from true to false for all port blocks
        for port_block in test_payload['data']:
            port_block['recordDel'] = False

        # Make API call with the updated payload
        response = TestVoyageItinerary.auth_api.voyage_itinerary(
            TestVoyageItinerary.imo, 
            TestVoyageItinerary.vesselname, 
            TestVoyageItinerary.vesselcode, 
            TestVoyageItinerary.voyagestatus, 
            test_payload
        )
        
        # Use common verification function
        TestVoyageItinerary.verify_api_response(response, "Voyage Itinerary API Test - Update RecordDel to False After Record Delete")

    @allure.title("Test Voyage Itinerary API - Update VIP_ARRIVAL_LOCAL of first port and VIP_DEPARTURE_LOCAL of last port block in combined payload of all test cases estimate id null")
    @allure.severity(allure.severity_level.NORMAL)
    def test_voyage_itinerary_update_first_last_port_estimate_id_null(self, setup_payload):
        """
        Test the voyage itinerary API by updating VIP_ARRIVAL_LOCAL of first port
        and VIP_DEPARTURE_LOCAL of last port block in combined payload of all test cases estimate id null
        """
        # Step 1: Get original payload (Test Case 1)
        original_payload = TestVoyageItinerary.test_case_full_payload_estimateId_null.copy()
        original_payload['data'] = [port.copy() for port in setup_payload['data']]
        
        # Step 2: Get updated payload (Test Case 2)
        test_case_11_payload = TestVoyageItinerary.test_case_11_payload.copy()
        
        # Step 3: Get test case 3 payload
        test_case_12_payload = TestVoyageItinerary.test_case_12_payload.copy()
        
        # Step 5: Combine all port data
        combined_ports = []
        
        # Add ports from original payload
        for port_block in original_payload['data']:
            combined_ports.append(port_block.copy())
        
        # Add ports from updated payload (excluding duplicates)
        existing_port_orders = {port['VIP_PORT_ORDER'] for port in combined_ports}
        for port_block in test_case_11_payload['data']:
            if port_block['VIP_PORT_ORDER'] not in existing_port_orders:
                combined_ports.append(port_block.copy())
                existing_port_orders.add(port_block['VIP_PORT_ORDER'])
        
        # Add ports from test case 3 (excluding duplicates)
        for port_block in test_case_12_payload['data']:
            if port_block['VIP_PORT_ORDER'] not in existing_port_orders:
                combined_ports.append(port_block.copy())
                existing_port_orders.add(port_block['VIP_PORT_ORDER'])
        
        # Sort ports by VIP_PORT_ORDER to identify first and last correctly
        combined_ports.sort(key=lambda x: x['VIP_PORT_ORDER'])
        
        if len(combined_ports) == 0:
            print("No ports available to update")
            return
        
        # Step 6: Filter out ports with recordDel: true FIRST
        filtered_ports = []
        ports_removed = []
        
        for port_block in combined_ports:
            if port_block.get('recordDel', False):
                ports_removed.append(port_block)
                print(f"Removed port: {port_block['VIP_PORT_NAME']} (Order: {port_block['VIP_PORT_ORDER']}) - recordDel: {port_block['recordDel']}")
            else:
                filtered_ports.append(port_block)
                print(f"Kept port: {port_block['VIP_PORT_NAME']} (Order: {port_block['VIP_PORT_ORDER']}) - recordDel: {port_block.get('recordDel', False)}")
        
        if len(filtered_ports) == 0:
            print("No ports available after filtering")
            return

        
        # Step 7: Update first port's VIP_ARRIVAL_LOCAL and last port's VIP_DEPARTURE_LOCAL on FILTERED ports
        first_port = filtered_ports[0]
        last_port = filtered_ports[-1]
        
        # Store original values for comparison
        original_first_arrival = first_port['VIP_ARRIVAL_LOCAL']
        original_last_departure = last_port['VIP_DEPARTURE_LOCAL']
        
        # Update first port arrival date (set to a past date within last month)
        from datetime import datetime, timedelta
        import random
        
        days_ago = random.randint(1, 30)
        original_first_arrival_date = datetime.strptime(original_first_arrival, '%Y-%m-%dT%H:%M:%S')
        new_arrival_date = original_first_arrival_date - timedelta(days=days_ago)
        new_arrival_str = new_arrival_date.strftime('%Y-%m-%dT%H:%M:%S')
        
        # Update last port departure date (set to a date after original first arrival)
        # Parse the original first arrival date to calculate departure
        original_last_departure_date = datetime.strptime(original_last_departure, '%Y-%m-%dT%H:%M:%S')
        days_after_arrival = random.randint(2, 5)
        new_departure_date = original_last_departure_date + timedelta(days=days_after_arrival)
        new_departure_str = new_departure_date.strftime('%Y-%m-%dT%H:%M:%S')
        
        # Apply updates to filtered ports
        first_port['VIP_ARRIVAL_LOCAL'] = new_arrival_str
        last_port['VIP_DEPARTURE_LOCAL'] = new_departure_str
        
        # Step 8: Create final payload with updated dates (filtered)
        final_payload = {
            "req_id": str(uuid.uuid4()),
            "isFullLoad": False,
            "data": filtered_ports
        }

         # Store the test case payload
        TestVoyageItinerary.test_case_full_payload_estimateId_null = final_payload.copy()
        
        # Step 9: Verify the updates
        if len(filtered_ports) > 0:
            updated_first_port = final_payload['data'][0]
            updated_last_port = final_payload['data'][-1]
            
            print(f"First port arrival updated from '{original_first_arrival}' to '{updated_first_port['VIP_ARRIVAL_LOCAL']}'")
            print(f"Last port departure updated from '{original_last_departure}' to '{updated_last_port['VIP_DEPARTURE_LOCAL']}'")
        else:
            print("No ports available after filtering")
            return
        
        # Make API call with the updated payload
        response = TestVoyageItinerary.auth_api.voyage_itinerary(
            TestVoyageItinerary.imo, 
            TestVoyageItinerary.vesselname, 
            TestVoyageItinerary.vesselcode, 
            TestVoyageItinerary.voyagestatus, 
            final_payload
        )
        
        # Use common verification function
        TestVoyageItinerary.verify_api_response(response, "Voyage Itinerary API Test with First Port Arrival and Last Port Departure Updates estimateId null")

    @allure.title("Test Voyage Itinerary API - Update VIP_VOYAGE_EST_ID for test_case_full_payload_estimateId_null")
    @allure.severity(allure.severity_level.NORMAL)
    def test_voyage_itinerary_update_vip_voyage_est_id_from_null(self, setup_payload):
        """
        Test the voyage itinerary API by updating VIP_VOYAGE_EST_ID 
        for the payload with estimateId null
        """
        # Get the test_case_full_payload_estimateId_null payload
        test_payload = TestVoyageItinerary.test_case_full_payload_estimateId_null.copy()
        test_payload['req_id'] = str(uuid.uuid4())
        
        # Generate a new VIP_VOYAGE_EST_ID value
        random_number = ''.join(random.choices(string.digits, k=8))
        new_voyage_est_id = f"{TestVoyageItinerary.imo}{random_number}{2026}"
        
        # Update VIP_VOYAGE_EST_ID for all port blocks
        for port_block in test_payload['data']:
            port_block['VIP_VOYAGE_EST_ID'] = new_voyage_est_id
        
        # Make API call with the updated payload
        response = TestVoyageItinerary.auth_api.voyage_itinerary(
            TestVoyageItinerary.imo, 
            TestVoyageItinerary.vesselname, 
            TestVoyageItinerary.vesselcode, 
            TestVoyageItinerary.voyagestatus, 
            test_payload
        )
        
        # Use common verification function
        TestVoyageItinerary.verify_api_response(response, "Voyage Itinerary API Test - Update VIP_VOYAGE_EST_ID from null estimate Id")

    @allure.title("Test Voyage Itinerary API - Update Estimate Id")
    @allure.severity(allure.severity_level.NORMAL)
    def test_voyage_itinerary_update_vip_voyage_est_id(self, setup_payload):
        """
        Test the voyage itinerary API by updating VIP_VOYAGE_EST_ID
        """
        # Get the test_case_full_payload_estimateId_null payload
        test_payload = TestVoyageItinerary.test_case_full_payload_estimateId_null.copy()
        test_payload['req_id'] = str(uuid.uuid4())
        
        # Generate a new VIP_VOYAGE_EST_ID value
        random_number = ''.join(random.choices(string.digits, k=8))
        new_voyage_est_id = f"{TestVoyageItinerary.imo}{random_number}{2026}"
        
        # Update VIP_VOYAGE_EST_ID for all port blocks
        for port_block in test_payload['data']:
            port_block['VIP_VOYAGE_EST_ID'] = new_voyage_est_id
        
        # Make API call with the updated payload
        response = TestVoyageItinerary.auth_api.voyage_itinerary(
            TestVoyageItinerary.imo, 
            TestVoyageItinerary.vesselname, 
            TestVoyageItinerary.vesselcode, 
            TestVoyageItinerary.voyagestatus, 
            test_payload
        )
        
        # Use common verification function
        TestVoyageItinerary.verify_api_response(response, "Voyage Itinerary API Test - Update VIP_VOYAGE_EST_ID")

    @allure.title("Test Voyage Itinerary API - Update Vessel Details with Same Estimate and Voyage")
    @allure.severity(allure.severity_level.NORMAL)
    def test_voyage_itinerary_update_vessel_details(self, setup_payload):
        """
        Test the voyage itinerary API by updating vessel details (IMO_NO, VIP_VSL_NAME, VIP_VSL_CODE)
        using the same estimateId and voyage number as test_voyage_itinerary_update_vip_voyage_est_id
        """
        # Get the test_case_full_payload_estimateId_null payload (same as used in test_voyage_itinerary_update_vip_voyage_est_id)
        test_payload = TestVoyageItinerary.test_case_full_payload_estimateId_null.copy()
        test_payload['req_id'] = str(uuid.uuid4())
        
        # Update vessel details, PK_HASH, and port details for all port blocks
        for i, port_block in enumerate(test_payload['data']):
            # Update vessel details
            port_block['IMO_NO'] = TestVoyageItinerary.new_imo_no
            port_block['VIP_VSL_NAME'] = TestVoyageItinerary.new_vsl_name
            port_block['VIP_VSL_CODE'] = TestVoyageItinerary.new_vsl_code
            
            # Generate new PK_HASH for each port
            new_pk_hash = f"{TestVoyageItinerary.new_imo_no}{random.randint(10000, 99999)}"
            port_block['PK_HASH'] = new_pk_hash
            
            # Update port order to ensure uniqueness
            port_block['VIP_PORT_ORDER'] = (i + 1) * 200
        
        # Make API call with the updated vessel details (using original vessel parameters for API call)
        response = TestVoyageItinerary.auth_api.voyage_itinerary(
            TestVoyageItinerary.imo,  # Original IMO for API authentication
            TestVoyageItinerary.vesselname,  # Original vessel name for API authentication
            TestVoyageItinerary.vesselcode,  # Original vessel code for API authentication
            TestVoyageItinerary.voyagestatus, 
            test_payload
        )
        
        # Use common verification function
        TestVoyageItinerary.verify_api_response(response, "Voyage Itinerary API Test - Update Vessel Details")

    @allure.title("Test Voyage Itinerary API - Port Function P Update")
    @allure.severity(allure.severity_level.NORMAL)
    def test_voyage_itinerary_port_function_p_update(self, setup_payload):
        """
        Test the voyage itinerary API by setting VIP_PORT_FUNC_DTL to 'P' 
        for one port
        """
        # Get the test_case_full_payload_estimateId_null payload
        test_payload = TestVoyageItinerary.test_case_full_payload_estimateId_null.copy()
        test_payload['req_id'] = str(uuid.uuid4())
        
        # Set VIP_PORT_FUNC_DTL to 'P' for first port only
        if len(test_payload['data']) >= 4:
            any_port = test_payload['data'][3]
            any_port['VIP_PORT_FUNC_DTL'] = 'P'
        else:
            print("No ports available to update")
            return
        
        # Make API call with the updated payload
        response = TestVoyageItinerary.auth_api.voyage_itinerary(
            TestVoyageItinerary.imo, 
            TestVoyageItinerary.vesselname, 
            TestVoyageItinerary.vesselcode, 
            TestVoyageItinerary.voyagestatus, 
            test_payload
        )
        
        # Use common verification function
        TestVoyageItinerary.verify_api_response(response, "Voyage Itinerary API Test - Port Function P Update")
      
    @allure.title("Test Voyage Itinerary API - Port Function I Update")
    @allure.severity(allure.severity_level.NORMAL)
    def test_voyage_itinerary_port_function_transit_port_update(self, setup_payload):
        """
        Test the voyage itinerary API by setting VIP_PORT_FUNC_DTL to 'I' 
        for one port
        """
        # Get the test_case_full_payload_estimateId_null payload
        test_payload = TestVoyageItinerary.test_case_full_payload_estimateId_null.copy()
        test_payload['req_id'] = str(uuid.uuid4())
        
        # Set VIP_PORT_FUNC_DTL to 'I' for one port (4th port)
        if len(test_payload['data']) >= 3:
            target_port = test_payload['data'][2]  # 4th port (index 3)
            target_port['VIP_PORT_FUNC_DTL'] = 'I'
        else:
            print("Need at least 4 ports to update 4th port to function 'I'")
            return
        
        # Make API call with the updated payload
        response = TestVoyageItinerary.auth_api.voyage_itinerary(
            TestVoyageItinerary.imo, 
            TestVoyageItinerary.vesselname, 
            TestVoyageItinerary.vesselcode, 
            TestVoyageItinerary.voyagestatus, 
            test_payload
        )
        
        # Use common verification function
        TestVoyageItinerary.verify_api_response(response, "Voyage Itinerary API Test - Port Function -Transit port Update")
      
    @allure.title("Test Voyage Itinerary API - Duplicate Port with Function L")
    @allure.severity(allure.severity_level.NORMAL)
    def test_voyage_itinerary_duplicate_port_function_l(self, setup_payload):
        """
        Test the voyage itinerary API by making first and second port the same
        and setting second port VIP_PORT_FUNC_DTL to 'L'
        """
        # Create a basic payload with 5 ports first
        test_payload = AuthPayloads.create_basic_payload(
            imo_no=TestVoyageItinerary.imo,
            vsl_name=TestVoyageItinerary.vesselname,
            vsl_code=TestVoyageItinerary.vesselcode,
            voyage_status=TestVoyageItinerary.voyagestatus,
            port_count=5
        )
        
        # Make the first and second ports the same
        if len(test_payload['data']) >= 2:
            # Copy first port data to second port
            first_port = test_payload['data'][0]
            second_port = test_payload['data'][1]
            
            # Copy all data from first port to second port except port_order, PK_HASH, and dates
            original_port_order = second_port['VIP_PORT_ORDER']
            original_pk_hash = second_port['PK_HASH']
            original_arrival = second_port['VIP_ARRIVAL_LOCAL']
            original_departure = second_port['VIP_DEPARTURE_LOCAL']
            
            # Update second port with first port's data
            for key, value in first_port.items():
                if key not in ['VIP_PORT_ORDER', 'PK_HASH', 'VIP_ARRIVAL_LOCAL', 'VIP_DEPARTURE_LOCAL']:
                    second_port[key] = value
            
            # Restore original port_order, PK_HASH, and dates
            second_port['VIP_PORT_ORDER'] = original_port_order
            second_port['PK_HASH'] = original_pk_hash
            second_port['VIP_ARRIVAL_LOCAL'] = original_arrival
            second_port['VIP_DEPARTURE_LOCAL'] = original_departure
            
            # Set second port function to 'L'
            second_port['VIP_PORT_FUNC_DTL'] = 'L'
            
            print(f"Made first and second ports the same:")
            print(f"  First port: {first_port['VIP_PORT_NAME']} (Order: {first_port['VIP_PORT_ORDER']})")
            print(f"  Second port: {second_port['VIP_PORT_NAME']} (Order: {second_port['VIP_PORT_ORDER']}, Function: L)")
        else:
            print("Need at least 2 ports to make first and second port same")
            return
        
        # Make API call with the updated payload
        response = TestVoyageItinerary.auth_api.voyage_itinerary(
            TestVoyageItinerary.imo, 
            TestVoyageItinerary.vesselname, 
            TestVoyageItinerary.vesselcode, 
            TestVoyageItinerary.voyagestatus, 
            test_payload
        )
        
        # Use common verification function
        TestVoyageItinerary.verify_api_response(response, "Voyage Itinerary API Test - Duplicate Port with Function L")
      
    @allure.title("Test Voyage Itinerary API - Null Arrival and Departure")
    @allure.severity(allure.severity_level.NORMAL)
    def test_voyage_itinerary_null_arrival_departure(self, setup_payload):
        """
        Test the voyage itinerary API by setting VIP_ARRIVAL_LOCAL and VIP_DEPARTURE_LOCAL to null
        """
        # Get the test_case_full_payload_estimateId_null payload
        test_payload = setup_payload.copy()
        test_payload['req_id'] = str(uuid.uuid4())

        random_number = ''.join(random.choices(string.digits, k=8))
        voyage_no = f"{TestVoyageItinerary.imo}{random_number}"
        estimate_id = f"{voyage_no}{2026}"

        # Set VIP_ARRIVAL_LOCAL and VIP_DEPARTURE_LOCAL to null for all port blocks
        for i, port_block in enumerate(test_payload['data']):
            # Store original values for comparison
            original_arrival = port_block.get('VIP_ARRIVAL_LOCAL')
            original_departure = port_block.get('VIP_DEPARTURE_LOCAL')
            
            # Set both to null
            port_block['VIP_ARRIVAL_LOCAL'] = None
            port_block['VIP_DEPARTURE_LOCAL'] = None
            port_block['VIP_VOYAGE_NO'] = voyage_no
            port_block['VIP_VOYAGE_EST_ID'] = estimate_id
            
            print(f"Port {i+1} ({port_block['VIP_PORT_NAME']}):")
            print(f"  VIP_ARRIVAL_LOCAL: {original_arrival} -> None")
            print(f"  VIP_DEPARTURE_LOCAL: {original_departure} -> None")
        
        print(f"Set arrival and departure to null for {len(test_payload['data'])} ports")
        
        # Make API call with the updated payload
        response = TestVoyageItinerary.auth_api.voyage_itinerary(
            TestVoyageItinerary.imo, 
            TestVoyageItinerary.vesselname, 
            TestVoyageItinerary.vesselcode, 
            TestVoyageItinerary.voyagestatus, 
            test_payload
        )
        
        # Use common verification function
        TestVoyageItinerary.verify_api_response(response, "Voyage Itinerary API Test - Null Arrival and Departure")
      
    @allure.title("Test Voyage Itinerary API - Multiple Same Ports with Different Functions")
    @allure.severity(allure.severity_level.NORMAL)
    def test_voyage_itinerary_multiple_same_ports_different_functions(self, setup_payload):
        """
        Test the voyage itinerary API by creating multiple ports with the same port data
        but different VIP_PORT_FUNC_DTL values (L, D, M)
        """
        # Create a basic payload with 5 ports first
        test_payload = AuthPayloads.create_basic_payload(
            imo_no=TestVoyageItinerary.imo,
            vsl_name=TestVoyageItinerary.vesselname,
            vsl_code=TestVoyageItinerary.vesselcode,
            voyage_status=TestVoyageItinerary.voyagestatus,
            port_count=5
        )
        
        # Make multiple ports the same with different functions
        if len(test_payload['data']) >= 3:
            # Use the first port as the base port data
            base_port = test_payload['data'][0]
            
            # Define the functions to assign
            functions_to_assign = ['L', 'D', 'M']
            
            # Update first 3 ports to be the same port with different functions
            for i in range(min(3, len(test_payload['data']))):
                current_port = test_payload['data'][i]
                
                # Store original unique identifiers and dates
                original_port_order = current_port['VIP_PORT_ORDER']
                original_pk_hash = current_port['PK_HASH']
                original_arrival = current_port['VIP_ARRIVAL_LOCAL']
                original_departure = current_port['VIP_DEPARTURE_LOCAL']
                
                # Copy all data from base port to current port except unique identifiers and dates
                for key, value in base_port.items():
                    if key not in ['VIP_PORT_ORDER', 'PK_HASH', 'VIP_ARRIVAL_LOCAL', 'VIP_DEPARTURE_LOCAL']:
                        current_port[key] = value
                
                # Restore original unique identifiers and dates
                current_port['VIP_PORT_ORDER'] = original_port_order
                current_port['PK_HASH'] = original_pk_hash
                current_port['VIP_ARRIVAL_LOCAL'] = original_arrival
                current_port['VIP_DEPARTURE_LOCAL'] = original_departure
                
                # Assign different function
                current_port['VIP_PORT_FUNC_DTL'] = functions_to_assign[i]
                
                print(f"Port {i+1}: {current_port['VIP_PORT_NAME']} (Order: {current_port['VIP_PORT_ORDER']}, Function: {functions_to_assign[i]})")
            
            print(f"Created 3 identical ports with different functions: L, D, M")
        else:
            print("Need at least 3 ports to create multiple same ports with different functions")
            return
        
        # Make API call with the updated payload
        response = TestVoyageItinerary.auth_api.voyage_itinerary(
            TestVoyageItinerary.imo, 
            TestVoyageItinerary.vesselname, 
            TestVoyageItinerary.vesselcode, 
            TestVoyageItinerary.voyagestatus, 
            test_payload
        )
        
        # Use common verification function
        TestVoyageItinerary.verify_api_response(response, "Voyage Itinerary API Test - Multiple Same Ports with Different Functions")
      
    @allure.title("Test Voyage Itinerary API - First and Last Port Same with Different Functions")
    @allure.severity(allure.severity_level.NORMAL)
    def test_voyage_itinerary_first_last_port_same_different_functions(self, setup_payload):
        """
        Test the voyage itinerary API by making first and last ports the same
        with first port having VIP_PORT_FUNC_DTL = C and last port having VIP_PORT_FUNC_DTL with L, D, or M
        """
        # Create a basic payload with 5 ports first
        test_payload = AuthPayloads.create_basic_payload(
            imo_no=TestVoyageItinerary.imo,
            vsl_name=TestVoyageItinerary.vesselname,
            vsl_code=TestVoyageItinerary.vesselcode,
            voyage_status=TestVoyageItinerary.voyagestatus,
            port_count=5
        )
        
        # Make first and last ports the same with different functions
        if len(test_payload['data']) >= 2:
            # Get first and last ports
            first_port = test_payload['data'][0]
            last_port = test_payload['data'][-1]
            
            # Store original unique identifiers and dates for last port
            original_port_order = last_port['VIP_PORT_ORDER']
            original_pk_hash = last_port['PK_HASH']
            original_arrival = last_port['VIP_ARRIVAL_LOCAL']
            original_departure = last_port['VIP_DEPARTURE_LOCAL']
            
            # Copy first port data to last port except unique identifiers and dates
            for key, value in first_port.items():
                if key not in ['VIP_PORT_ORDER', 'PK_HASH', 'VIP_ARRIVAL_LOCAL', 'VIP_DEPARTURE_LOCAL']:
                    last_port[key] = value
            
            # Restore original unique identifiers and dates for last port
            last_port['VIP_PORT_ORDER'] = original_port_order
            last_port['PK_HASH'] = original_pk_hash
            last_port['VIP_ARRIVAL_LOCAL'] = original_arrival
            last_port['VIP_DEPARTURE_LOCAL'] = original_departure
            
            # Set first port function to 'C' (Cargo)
            first_port['VIP_PORT_FUNC_DTL'] = 'C'
            
            # Set last port function to random choice from L, D, M
            last_port_functions = ['L', 'D', 'M']
            last_port_function = random.choice(last_port_functions)
            last_port['VIP_PORT_FUNC_DTL'] = last_port_function
            
            print(f"Made first and last ports the same with different functions:")
            print(f"  First port: {first_port['VIP_PORT_NAME']} (Order: {first_port['VIP_PORT_ORDER']}, Function: C)")
            print(f"  Last port: {last_port['VIP_PORT_NAME']} (Order: {last_port['VIP_PORT_ORDER']}, Function: {last_port_function})")
        else:
            print("Need at least 2 ports to make first and last port same")
            return
        
        # Make API call with the updated payload
        response = TestVoyageItinerary.auth_api.voyage_itinerary(
            TestVoyageItinerary.imo, 
            TestVoyageItinerary.vesselname, 
            TestVoyageItinerary.vesselcode, 
            TestVoyageItinerary.voyagestatus, 
            test_payload
        )
        
        # Use common verification function
        TestVoyageItinerary.verify_api_response(response, "Voyage Itinerary API Test - First and Last Port Same with Different Functions")
     