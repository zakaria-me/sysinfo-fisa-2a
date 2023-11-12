<?php

namespace App\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\Routing\Annotation\Route;
use Symfony\Component\HttpClient\HttpClient;
use Symfony\Component\HttpFoundation\Request;

class SoapController extends AbstractController
{

    /**
     * @Route("/soap/service", name="soap_service", methods={"POST"})
     */
    public function soapService(Request $request)
    {
        // Get the raw SOAP request content
        $soapRequestContent = $request->getContent();

        // Process the SOAP request as needed
        $soapResponseContent = $this->processSoapRequest($soapRequestContent);

        // Create a new Response with the SOAP response content
        $response = new Response($soapResponseContent);

        // Set the appropriate headers for a SOAP response
        $response->headers->set('Content-Type', 'text/xml; charset=UTF-8');

        return $response;
    }

    /**
     * Process the SOAP request and generate a SOAP response.
     *
     * @param string $soapRequestContent The raw content of the SOAP request.
     *
     * @return string The raw content of the SOAP response.
     */
    private function processSoapRequest($soapRequestContent)
    {
        // Implement your logic to process the SOAP request and generate the SOAP response.
        // You might use a SOAP server library or manually construct the SOAP response.

        // For demonstration purposes, this example simply echoes the received SOAP request.
        $soapResponseContent = sprintf(
            '<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" 
                                xmlns:xsd="http://www.w3.org/2001/XMLSchema" 
                                xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
                <SOAP-ENV:Body>
                    <Response>Hello, SOAP Client! You sent: %s</Response>
                </SOAP-ENV:Body>
            </SOAP-ENV:Envelope>',
            htmlspecialchars($soapRequestContent)
        );

        return $soapResponseContent;
    }

    /**
     * @Route("/soap/rest-call", name="soap_rest_call")
     */
    public function soapRestCall()
    {
        $httpClient = HttpClient::create();
        
        // Define the REST API endpoint
        $apiEndpoint = 'https://api.example.com/data';

        // Make a GET request to the REST API
        $response = $httpClient->request('GET', $apiEndpoint);

        // Check if the request was successful (status code 200)
        if ($response->getStatusCode() == 200) {
            // Parse the JSON response
            $data = $response->toArray();

            // Handle the data as needed
            // ...

            return new JsonResponse(['message' => 'REST API call successful', 'data' => $data]);
        } else {
            // Handle the error
            $errorMessage = 'Error calling REST API: ' . $response->getStatusCode();
            return new JsonResponse(['error' => $errorMessage], $response->getStatusCode());
        }
    }

    #[Route('/soap', name: 'app_soap')]
    public function index(): JsonResponse
    {
        return $this->json([
            'message' => 'Welcome to your new controller!',
            'path' => 'src/Controller/SoapController.php',
        ]);
    }
}
