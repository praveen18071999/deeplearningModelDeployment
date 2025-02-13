'use client'
import React, { useState } from 'react'
import { ImageUpload } from '@/components/image-upload'
import { PredictionsTable } from '@/components/predictions-table'
import { Progress } from '@/components/ui/progress'
import Image from 'next/image'

export default function PredictionsPage() {
  const [uploadedImage, setUploadedImage] = useState<string | null>(null)
  const [predictions, setPredictions] = useState<{ [key: string]: string }>({})
  const [isLoading, setIsLoading] = useState(false)

  const handleUpload = async (file: File) => {
    setIsLoading(true)
    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await fetch('http://142.93.244.44/api/predict/', {
        method: 'POST',
        body: formData,
      })
      const data = await response.json()
      console.log(data)
      setPredictions(data.predictions)
      setUploadedImage(URL.createObjectURL(file))
    } catch (error) {
      console.error('Error:', error)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-4">Chest X-ray Predictions</h1>
      <div className="space-y-4">
        <ImageUpload onUpload={handleUpload} />
        <div className="mt-4">
          {uploadedImage ? (
            <Image
              src={uploadedImage || "/placeholder.svg"}
              alt="Uploaded chest X-ray"
              width={200}
              height={200}
              className="max-w-full max-h-full object-contain"
            />
          ) : (
            <p className="text-gray-400">No image uploaded yet</p>
          )}
        </div>
        <div>
          <h2 className="text-2xl font-semibold mb-4">Predictions</h2>
          {isLoading ? (
            <div className="flex items-center justify-center h-64">
              <Progress value={33} />
            </div>
          ) : (
            <>
              <p className="mb-4 text-sm text-gray-600">
                The table below shows the probability of each condition being present in the uploaded chest X-ray image.
                Higher percentages indicate a greater likelihood of the condition being present.
              </p>
              <PredictionsTable predictions={predictions} />
            </>
          )}
        </div>
      </div>
    </div>
  )
}