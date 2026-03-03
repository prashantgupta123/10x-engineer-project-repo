import { useState, useEffect } from 'react';
import { api } from '../api/client';

export const usePrompts = (filters = {}) => {
  const [prompts, setPrompts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchPrompts = async () => {
    try {
      setLoading(true);
      const data = await api.getPrompts(filters);
      setPrompts(data.prompts);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPrompts();
  }, [JSON.stringify(filters)]);

  return { prompts, loading, error, refetch: fetchPrompts };
};

export const useCollections = () => {
  const [collections, setCollections] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchCollections = async () => {
    try {
      setLoading(true);
      const data = await api.getCollections();
      setCollections(data.collections);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCollections();
  }, []);

  return { collections, loading, error, refetch: fetchCollections };
};
