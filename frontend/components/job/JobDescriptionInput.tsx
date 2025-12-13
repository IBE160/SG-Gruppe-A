'use client';

import React from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import axios from 'axios';
import { useRouter } from 'next/navigation';
import toast from 'react-hot-toast';
import { createClient } from '@/utils/supabase/client';

// Define validation schema
const formSchema = z.object({
  jobDescription: z.string()
    .min(5, 'Job description must be at least 5 characters.')
    .max(10000, 'Job description is too long.'),
});

type FormData = z.infer<typeof formSchema>;

export default function JobDescriptionInput() {
  const router = useRouter();
  const { 
    register, 
    handleSubmit, 
    formState: { errors, isSubmitting }, 
    reset 
  } = useForm<FormData>({
    resolver: zodResolver(formSchema),
  });

  const onSubmit = async (data: FormData) => {
    try {
      const supabase = createClient();
      const { data: { session } } = await supabase.auth.getSession();
      const token = session?.access_token;

      if (!token) {
        toast.error('You must be logged in to save a job description.');
        return;
      }
      
      const config = {
        headers: {
          Authorization: `Bearer ${token}`
        }
      };

      const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';
      const response = await axios.post(`${API_URL}/api/job-description/`, {
        content: data.jobDescription,
      }, config);
      console.log('Job description saved:', response.data);
      toast.success('Job description saved successfully!');
      reset(); // Clear the form
      router.refresh(); // Refresh current route to show changes if any
    } catch (error: any) {
      console.error('Failed to save job description:', error.response?.data || error.message);
      toast.error(`Failed to save job description: ${error.response?.data?.detail || error.message}`);
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-4 bg-white shadow-md rounded-lg">
      <h2 className="text-2xl font-bold mb-4 text-gray-900">Paste Job Description</h2>
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        <div>
          <label htmlFor="jobDescription" className="block text-sm font-medium text-gray-800">
            Job Description
          </label>
          <textarea
            id="jobDescription"
            {...register('jobDescription')}
            rows={10}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2 text-gray-800 placeholder-gray-800"
            placeholder="Paste your job description here..."
            disabled={isSubmitting}
          />
          {errors.jobDescription && (
            <p className="mt-1 text-sm text-red-600">{errors.jobDescription.message}</p>
          )}
        </div>
        <div>
          <button
            type="submit"
            className="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
            disabled={isSubmitting}
          >
            {isSubmitting ? 'Saving...' : 'Save Job Description'}
          </button>
        </div>
      </form>
    </div>
  );
}