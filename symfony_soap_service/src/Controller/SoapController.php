<?php

// src/Controller/SoapController.php
namespace App\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Annotation\Route;
use Symfony\Component\HttpFoundation\Request;

/**
 * @Route("/soap")
 */
class SoapController extends AbstractController
{
    /**
     * @Route("/service", name="soap_service", methods={"POST"})
     */
    public function soapService(Request $request): Response
    {
        $soapRequest = $request->getContent(); // Retrieve the SOAP request

        // Process the SOAP request and generate a SOAP response
        $soapResponse = '<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">
                            <SOAP-ENV:Body>
                                <exampleResponse>Hello, SOAP World!</exampleResponse>
                            </SOAP-ENV:Body>
                        </SOAP-ENV:Envelope>';

        return new Response($soapResponse, 200, ['Content-Type' => 'text/xml']);
    }
}

