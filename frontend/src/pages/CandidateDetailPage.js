import React, { useState, useEffect } from 'react';
import { 
  Container, 
  Box, 
  Typography, 
  Paper, 
  Button, 
  AppBar, 
  Toolbar, 
  IconButton, 
  Drawer,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Divider,
  CircularProgress,
  Alert,
  Grid,
  Card,
  CardContent,
  Breadcrumbs,
  Link
} from '@mui/material';
import { 
  Menu as MenuIcon, 
  Dashboard as DashboardIcon,
  Person as PersonIcon,
  Work as WorkIcon,
  ExitToApp as LogoutIcon,
  ArrowBack as ArrowBackIcon
} from '@mui/icons-material';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate, useParams } from 'react-router-dom';
import axios from 'axios';

const CandidateDetailPage = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const { id } = useParams();
  const [drawerOpen, setDrawerOpen] = useState(false);
  const [candidate, setCandidate] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchCandidate = async () => {
      try {
        setLoading(true);
        const response = await axios.get(`/api/candidates/${id}`);
        setCandidate(response.data);
        setError('');
      } catch (err) {
        console.error('Error fetching candidate:', err);
        setError('Failed to load candidate details. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    fetchCandidate();
  }, [id]);

  const toggleDrawer = () => {
    setDrawerOpen(!drawerOpen);
  };

  const navigateTo = (path) => {
    navigate(path);
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'Not specified';
    const date = new Date(dateString);
    return date.toLocaleDateString();
  };

  const drawerContent = (
    <Box sx={{ width: 250 }} role="presentation">
      <Box sx={{ p: 2 }}>
        <Typography variant="h6" color="primary">Sombra Recruitment</Typography>
        <Typography variant="body2" color="text.secondary">
          {user?.email}
        </Typography>
      </Box>
      <Divider />
      <List>
        <ListItem button onClick={() => navigateTo('/dashboard')}>
          <ListItemIcon>
            <DashboardIcon />
          </ListItemIcon>
          <ListItemText primary="Dashboard" />
        </ListItem>
        <ListItem button selected onClick={() => navigateTo('/candidates')}>
          <ListItemIcon>
            <PersonIcon color="primary" />
          </ListItemIcon>
          <ListItemText primary="Candidates" />
        </ListItem>
        <ListItem button onClick={() => navigateTo('/job-vacancies')}>
          <ListItemIcon>
            <WorkIcon />
          </ListItemIcon>
          <ListItemText primary="Job Vacancies" />
        </ListItem>
      </List>
      <Divider />
      <List>
        <ListItem button onClick={logout}>
          <ListItemIcon>
            <LogoutIcon />
          </ListItemIcon>
          <ListItemText primary="Logout" />
        </ListItem>
      </List>
    </Box>
  );

  const renderCandidateDetails = () => {
    if (!candidate) return null;

    return (
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h5" gutterBottom>Basic Information</Typography>
              <Grid container spacing={2}>
                <Grid item xs={12} md={6}>
                  <Typography variant="subtitle2" color="text.secondary">Professional Code</Typography>
                  <Typography variant="body1">{candidate.codigo_profissional || 'Not specified'}</Typography>
                </Grid>
                <Grid item xs={12} md={6}>
                  <Typography variant="subtitle2" color="text.secondary">Name</Typography>
                  <Typography variant="body1">{candidate.nome || 'Not specified'}</Typography>
                </Grid>
                <Grid item xs={12} md={6}>
                  <Typography variant="subtitle2" color="text.secondary">Email</Typography>
                  <Typography variant="body1">{candidate.email || 'Not specified'}</Typography>
                </Grid>
                <Grid item xs={12} md={6}>
                  <Typography variant="subtitle2" color="text.secondary">Secondary Email</Typography>
                  <Typography variant="body1">{candidate.email_secundario || 'Not specified'}</Typography>
                </Grid>
                <Grid item xs={12} md={6}>
                  <Typography variant="subtitle2" color="text.secondary">Phone</Typography>
                  <Typography variant="body1">{candidate.telefone || 'Not specified'}</Typography>
                </Grid>
                <Grid item xs={12} md={6}>
                  <Typography variant="subtitle2" color="text.secondary">Mobile Phone</Typography>
                  <Typography variant="body1">{candidate.telefone_celular || 'Not specified'}</Typography>
                </Grid>
                <Grid item xs={12} md={6}>
                  <Typography variant="subtitle2" color="text.secondary">Alternative Phone</Typography>
                  <Typography variant="body1">{candidate.telefone_recado || 'Not specified'}</Typography>
                </Grid>
                <Grid item xs={12} md={6}>
                  <Typography variant="subtitle2" color="text.secondary">Gender</Typography>
                  <Typography variant="body1">{candidate.sexo || 'Not specified'}</Typography>
                </Grid>
                <Grid item xs={12} md={6}>
                  <Typography variant="subtitle2" color="text.secondary">Date of Birth</Typography>
                  <Typography variant="body1">{formatDate(candidate.data_nascimento)}</Typography>
                </Grid>
                <Grid item xs={12} md={6}>
                  <Typography variant="subtitle2" color="text.secondary">Marital Status</Typography>
                  <Typography variant="body1">{candidate.estado_civil || 'Not specified'}</Typography>
                </Grid>
                <Grid item xs={12} md={6}>
                  <Typography variant="subtitle2" color="text.secondary">CPF</Typography>
                  <Typography variant="body1">{candidate.cpf || 'Not specified'}</Typography>
                </Grid>
                <Grid item xs={12} md={6}>
                  <Typography variant="subtitle2" color="text.secondary">PCD (Person with Disability)</Typography>
                  <Typography variant="body1">{candidate.pcd || 'Not specified'}</Typography>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h5" gutterBottom>Contact Information</Typography>
              <Grid container spacing={2}>
                <Grid item xs={12}>
                  <Typography variant="subtitle2" color="text.secondary">Address</Typography>
                  <Typography variant="body1">{candidate.endereco || 'Not specified'}</Typography>
                </Grid>
                <Grid item xs={12} md={6}>
                  <Typography variant="subtitle2" color="text.secondary">Skype</Typography>
                  <Typography variant="body1">{candidate.skype || 'Not specified'}</Typography>
                </Grid>
                <Grid item xs={12} md={6}>
                  <Typography variant="subtitle2" color="text.secondary">LinkedIn</Typography>
                  <Typography variant="body1">{candidate.url_linkedin || 'Not specified'}</Typography>
                </Grid>
                <Grid item xs={12} md={6}>
                  <Typography variant="subtitle2" color="text.secondary">Facebook</Typography>
                  <Typography variant="body1">{candidate.facebook || 'Not specified'}</Typography>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h5" gutterBottom>Professional Information</Typography>
              <Grid container spacing={2}>
                <Grid item xs={12} md={6}>
                  <Typography variant="subtitle2" color="text.secondary">Professional Title</Typography>
                  <Typography variant="body1">{candidate.titulo_profissional || 'Not specified'}</Typography>
                </Grid>
                <Grid item xs={12} md={6}>
                  <Typography variant="subtitle2" color="text.secondary">Area of Expertise</Typography>
                  <Typography variant="body1">{candidate.area_atuacao || 'Not specified'}</Typography>
                </Grid>
                <Grid item xs={12} md={6}>
                  <Typography variant="subtitle2" color="text.secondary">Professional Level</Typography>
                  <Typography variant="body1">{candidate.nivel_profissional || 'Not specified'}</Typography>
                </Grid>
                <Grid item xs={12} md={6}>
                  <Typography variant="subtitle2" color="text.secondary">Current Position</Typography>
                  <Typography variant="body1">{candidate.cargo_atual || 'Not specified'}</Typography>
                </Grid>
                <Grid item xs={12} md={6}>
                  <Typography variant="subtitle2" color="text.secondary">Current Project</Typography>
                  <Typography variant="body1">{candidate.projeto_atual || 'Not specified'}</Typography>
                </Grid>
                <Grid item xs={12} md={6}>
                  <Typography variant="subtitle2" color="text.secondary">Client</Typography>
                  <Typography variant="body1">{candidate.cliente || 'Not specified'}</Typography>
                </Grid>
                <Grid item xs={12} md={6}>
                  <Typography variant="subtitle2" color="text.secondary">Unit</Typography>
                  <Typography variant="body1">{candidate.unidade || 'Not specified'}</Typography>
                </Grid>
                <Grid item xs={12} md={6}>
                  <Typography variant="subtitle2" color="text.secondary">Remuneration</Typography>
                  <Typography variant="body1">{candidate.remuneracao ? `R$ ${candidate.remuneracao}` : 'Not specified'}</Typography>
                </Grid>
                <Grid item xs={12} md={6}>
                  <Typography variant="subtitle2" color="text.secondary">Professional Goal</Typography>
                  <Typography variant="body1">{candidate.objetivo_profissional || 'Not specified'}</Typography>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h5" gutterBottom>Skills and Qualifications</Typography>
              <Grid container spacing={2}>
                <Grid item xs={12}>
                  <Typography variant="subtitle2" color="text.secondary">Technical Knowledge</Typography>
                  <Typography variant="body1">{candidate.conhecimentos_tecnicos || 'Not specified'}</Typography>
                </Grid>
                <Grid item xs={12}>
                  <Typography variant="subtitle2" color="text.secondary">Certifications</Typography>
                  <Typography variant="body1">{candidate.certificacoes || 'Not specified'}</Typography>
                </Grid>
                <Grid item xs={12}>
                  <Typography variant="subtitle2" color="text.secondary">Other Certifications</Typography>
                  <Typography variant="body1">{candidate.outras_certificacoes || 'Not specified'}</Typography>
                </Grid>
                <Grid item xs={12}>
                  <Typography variant="subtitle2" color="text.secondary">Qualifications</Typography>
                  <Typography variant="body1">{candidate.qualificacoes || 'Not specified'}</Typography>
                </Grid>
                <Grid item xs={12}>
                  <Typography variant="subtitle2" color="text.secondary">Experiences</Typography>
                  <Typography variant="body1">{candidate.experiencias || 'Not specified'}</Typography>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h5" gutterBottom>Education and Languages</Typography>
              <Grid container spacing={2}>
                <Grid item xs={12} md={6}>
                  <Typography variant="subtitle2" color="text.secondary">Academic Level</Typography>
                  <Typography variant="body1">{candidate.nivel_academico || 'Not specified'}</Typography>
                </Grid>
                <Grid item xs={12} md={6}>
                  <Typography variant="subtitle2" color="text.secondary">Other Courses</Typography>
                  <Typography variant="body1">{candidate.outro_curso || 'Not specified'}</Typography>
                </Grid>
                <Grid item xs={12} md={4}>
                  <Typography variant="subtitle2" color="text.secondary">English Level</Typography>
                  <Typography variant="body1">{candidate.nivel_ingles || 'Not specified'}</Typography>
                </Grid>
                <Grid item xs={12} md={4}>
                  <Typography variant="subtitle2" color="text.secondary">Spanish Level</Typography>
                  <Typography variant="body1">{candidate.nivel_espanhol || 'Not specified'}</Typography>
                </Grid>
                <Grid item xs={12} md={4}>
                  <Typography variant="subtitle2" color="text.secondary">Other Languages</Typography>
                  <Typography variant="body1">{candidate.outro_idioma !== '-' ? candidate.outro_idioma : 'Not specified'}</Typography>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h5" gutterBottom>System Information</Typography>
              <Grid container spacing={2}>
                <Grid item xs={12} md={6}>
                  <Typography variant="subtitle2" color="text.secondary">Creation Date</Typography>
                  <Typography variant="body1">{formatDate(candidate.data_criacao)}</Typography>
                </Grid>
                <Grid item xs={12} md={6}>
                  <Typography variant="subtitle2" color="text.secondary">Last Update</Typography>
                  <Typography variant="body1">{formatDate(candidate.data_atualizacao)}</Typography>
                </Grid>
                <Grid item xs={12} md={6}>
                  <Typography variant="subtitle2" color="text.secondary">Inserted By</Typography>
                  <Typography variant="body1">{candidate.inserido_por || 'Not specified'}</Typography>
                </Grid>
                <Grid item xs={12} md={6}>
                  <Typography variant="subtitle2" color="text.secondary">Source</Typography>
                  <Typography variant="body1">{candidate.sabendo_de_nos_por || 'Not specified'}</Typography>
                </Grid>
                <Grid item xs={12} md={6}>
                  <Typography variant="subtitle2" color="text.secondary">Indication Source</Typography>
                  <Typography variant="body1">{candidate.fonte_indicacao !== ':' ? candidate.fonte_indicacao : 'Not specified'}</Typography>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    );
  };

  return (
    <Box sx={{ display: 'flex' }}>
      <AppBar position="fixed">
        <Toolbar>
          <IconButton
            color="inherit"
            aria-label="open drawer"
            edge="start"
            onClick={toggleDrawer}
            sx={{ mr: 2 }}
          >
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" noWrap component="div">
            Candidate Details
          </Typography>
          <Box sx={{ flexGrow: 1 }} />
          <Button color="inherit" onClick={logout}>
            Logout
          </Button>
        </Toolbar>
      </AppBar>
      
      <Drawer
        anchor="left"
        open={drawerOpen}
        onClose={toggleDrawer}
      >
        {drawerContent}
      </Drawer>
      
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          p: 3,
          mt: 8,
          backgroundColor: (theme) => theme.palette.background.default,
          minHeight: '100vh'
        }}
      >
        <Container maxWidth="lg">
          <Box sx={{ mb: 3 }}>
            <Breadcrumbs aria-label="breadcrumb">
              <Link 
                color="inherit" 
                sx={{ cursor: 'pointer' }}
                onClick={() => navigateTo('/dashboard')}
              >
                Dashboard
              </Link>
              <Link 
                color="inherit" 
                sx={{ cursor: 'pointer' }}
                onClick={() => navigateTo('/candidates')}
              >
                Candidates
              </Link>
              <Typography color="text.primary">Candidate Details</Typography>
            </Breadcrumbs>
          </Box>
          
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
            <Button 
              variant="outlined" 
              startIcon={<ArrowBackIcon />}
              onClick={() => navigateTo('/candidates')}
              sx={{ mr: 2 }}
            >
              Back to Candidates
            </Button>
            <Typography variant="h4">
              {loading ? 'Loading...' : candidate?.nome || 'Candidate Details'}
            </Typography>
          </Box>
          
          {error && (
            <Alert severity="error" sx={{ mb: 3 }}>
              {error}
            </Alert>
          )}
          
          {loading ? (
            <Box display="flex" justifyContent="center" my={5}>
              <CircularProgress />
            </Box>
          ) : (
            renderCandidateDetails()
          )}
        </Container>
      </Box>
    </Box>
  );
};

export default CandidateDetailPage;
